import click
import pandas
import sys
import logging
import logging.config
import os
from taxi_rides_outlier_detection import outlier_detector
from datetime import datetime
import json
from taxi_rides_outlier_detection import monitoring


if os.path.exists('logging.conf'):
    logging.config.fileConfig('logging.conf')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@click.command()
@click.argument('data_dir', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.argument('date', type=click.STRING, required=False)
def detect_outliers(data_dir: str, date: str):
    logger = logging.getLogger(__name__)
    if(date is None):
        date = datetime.now().strftime("%Y-%m-%d")
    input_file = os.path.join(data_dir, f"{date}.taxi-rides.parquet")
    logger.info(f"Processing taxi ride data from: {input_file}")
    data = pandas.read_parquet(input_file)

    logger.info("Detecting outliers")
    outliers, metadata = outlier_detector.detect_outliers(data)
    logger.info("Detected %s outliers", len(outliers))

    outliers_output_file = os.path.join(data_dir, f"{date}.taxi-rides.outliers.parquet")
    logger.info(f"Writing outliers to: {outliers_output_file}")
    outliers.to_parquet(outliers_output_file, index=False)

    metadata_output_file = os.path.join(data_dir, f"{date}.taxi-rides.run-metadata.json")
    logger.info(f"Writing metadata to: {metadata_output_file}")
    with open(metadata_output_file, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)


@click.command()
@click.argument('data_dir', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.argument('date', type=click.STRING, required=False)
@click.option('--evidently-project-id', required=False, type=click.STRING, help='The evidently project id where the snapshot should be saved to')
def detect_input_data_drift(data_dir: str, date: str, evidently_project_id: str):
    logger = logging.getLogger(__name__)
    if(date is None):
        date = datetime.now().strftime("%Y-%m-%d")
    input_file = os.path.join(data_dir, f"{date}.taxi-rides.parquet")
    logger.info(f"Processing taxi ride data from: {input_file}")
    data = pandas.read_parquet(input_file)

    module_dir = os.path.dirname(os.path.abspath(__file__))
    reference_data = pandas.read_parquet(os.path.join(module_dir, "reference.taxi-rides.parquet"))

    logger.info("Detecting input data drift")
    result = monitoring.detect_drift(reference_data, data, datetime.strptime(date, "%Y-%m-%d"))

    drift_html_output_file = os.path.join(data_dir, f"{date}.taxi-rides.drift-report.html")
    logger.info(f"Writing results to: {drift_html_output_file}")    
    result.save_html(drift_html_output_file)
    
    drift_json_output_file = os.path.join(data_dir, f"{date}.taxi-rides.drift-report.json")
    logger.info(f"Writing results to: {drift_json_output_file}")    
    result.save_json(drift_json_output_file)

    if evidently_project_id is not None:
        from evidently.ui.workspace import Workspace
        logger.info(f"Recording data drift snapshot")    
        workspace = Workspace("workspace")
        workspace.add_run(evidently_project_id, result)
