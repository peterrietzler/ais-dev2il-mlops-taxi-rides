import click
import pandas
import sys
import logging
import logging.config
import os
from taxi_rides_outlier_detection import outlier_detector
from datetime import datetime
import json

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