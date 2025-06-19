import click
import mlflow
import pandas
import logging
import logging.config
import os
from taxi_rides_outlier_detection import outlier_detector
from datetime import datetime
import json
from taxi_rides_outlier_detection import monitoring
from taxi_rides_outlier_detection import outlier_detector_classifier
import pickle


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
        logger.info("Recording data drift snapshot")    
        workspace = Workspace("workspace")
        workspace.add_run(evidently_project_id, result)


@click.command()
@click.argument('labeled_data_file', type=click.Path(exists=True, dir_okay=False, file_okay=True))
@click.argument('model_output_file', type=click.STRING, required=True)
def train_random_forest_classifier(labeled_data_file: str, model_output_file: str):
    logger = logging.getLogger(__name__)
    logger.info(f"Processing taxi ride data from: {labeled_data_file}")
    data = pandas.read_parquet(labeled_data_file)

    logger.info("Training outlier detection classifier")
    mlflow.set_experiment("random-forest-classifier")
    # turn on auto logging models. See https://mlflow.org/docs/latest/ml/tracking/autolog
    mlflow.autolog()
    with mlflow.start_run():
        model, metadata = outlier_detector_classifier.train_random_forest_classifier(data)
        # log the data used for training
        mlflow.log_artifact(labeled_data_file)
        # log some custom metrics
        for false_key, false_value in metadata["False"].items():
            mlflow.log_metric(f"False_{false_key}", false_value)
        for false_key, false_value in metadata["True"].items():
            mlflow.log_metric(f"True_{false_key}", false_value)
    logger.info("Model training completed")
    
    logger.info("Storing model to %s", model_output_file)
    with open(model_output_file, "wb") as f:
        pickle.dump(model, f)

    metadata_output_file = f"{model_output_file}.metadata.json"
    logger.info(f"Writing metadata to: {metadata_output_file}")
    with open(metadata_output_file, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)

@click.command()
@click.argument('labeled_data_file', type=click.Path(exists=True, dir_okay=False, file_okay=True))
@click.argument('model_output_file', type=click.STRING, required=True)
def train_random_forest_classifier_v2(labeled_data_file: str, model_output_file: str):
    logger = logging.getLogger(__name__)
    logger.info(f"Processing taxi ride data from: {labeled_data_file}")
    data = pandas.read_parquet(labeled_data_file)

    logger.info("Training outlier detection classifier")
    mlflow.set_experiment("random-forest-classifier-v2")
    mlflow.autolog()
    with mlflow.start_run():
        model, metadata = outlier_detector_classifier.train_random_forest_classifier_v2(data)
        # log the data used for training
        mlflow.log_artifact(labeled_data_file)
        # log some custom metrics
        for false_key, false_value in metadata["False"].items():
            mlflow.log_metric(f"False_{false_key}", false_value)
        for false_key, false_value in metadata["True"].items():
            mlflow.log_metric(f"True_{false_key}", false_value)
    logger.info("Model training completed")
    
    logger.info("Storing model to %s", model_output_file)
    with open(model_output_file, "wb") as f:
        pickle.dump(model, f)

    metadata_output_file = f"{model_output_file}.metadata.json"
    logger.info(f"Writing metadata to: {metadata_output_file}")
    with open(metadata_output_file, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)

@click.command()
@click.argument('labeled_data_file', type=click.Path(exists=True, dir_okay=False, file_okay=True))
@click.argument('model_output_file', type=click.STRING, required=True)
def train_logistic_regression_classifier(labeled_data_file: str, model_output_file: str):
    logger = logging.getLogger(__name__)
    logger.info(f"Processing taxi ride data from: {labeled_data_file}")
    data = pandas.read_parquet(labeled_data_file)

    logger.info("Training outlier detection classifier")
    mlflow.set_experiment("logistic-regression-classifier")
    mlflow.autolog()
    with mlflow.start_run():
        model, metadata = outlier_detector_classifier.train_logistic_regression_classifier(data)
        # log the data used for training
        mlflow.log_artifact(labeled_data_file)
        # log some custom metrics
        for false_key, false_value in metadata["False"].items():
            mlflow.log_metric(f"False_{false_key}", false_value)
        for false_key, false_value in metadata["True"].items():
            mlflow.log_metric(f"True_{false_key}", false_value)
    logger.info("Model training completed")
    
    logger.info("Storing model to %s", model_output_file)
    with open(model_output_file, "wb") as f:
        pickle.dump(model, f)

    metadata_output_file = f"{model_output_file}.metadata.json"
    logger.info(f"Writing metadata to: {metadata_output_file}")
    with open(metadata_output_file, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)


@click.command()
@click.argument('model_file', type=click.Path(exists=True, dir_okay=False, file_okay=True))
@click.argument('data_dir', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.argument('date', type=click.STRING, required=False)
def detect_outliers_with_classifier(model_file: str, data_dir: str, date: str):
    logger = logging.getLogger(__name__)
    if(date is None):
        date = datetime.now().strftime("%Y-%m-%d")
    input_file = os.path.join(data_dir, f"{date}.taxi-rides.parquet")
    logger.info(f"Processing taxi ride data from: {input_file}")
    data = pandas.read_parquet(input_file)

    logger.info("Loading outlier detection classifier from %s", model_file)
    with open(model_file, "rb") as f:
        model = pickle.load(f)

    logger.info("Detecting outliers")
    outliers = outlier_detector_classifier.detect_outliers(data, model)
    logger.info("Detected %s outliers", len(outliers))

    outliers_output_file = os.path.join(data_dir, f"{date}.taxi-rides.outliers.parquet")
    logger.info(f"Writing outliers to: {outliers_output_file}")
    outliers.to_parquet(outliers_output_file, index=False)