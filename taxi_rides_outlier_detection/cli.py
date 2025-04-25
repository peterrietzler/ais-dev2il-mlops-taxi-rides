import click
import pandas
import sys
import logging
import logging.config
import os
from taxi_rides_outlier_detection import outlier_detector

def _setup_logging():
    if os.path.exists('logging.conf'):
        logging.config.fileConfig('logging.conf')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@click.command()
@click.argument('input_file', type=click.STRING, required=True)
def detect_outliers(input_file):
    _setup_logging()
    
    logger = logging.getLogger(__name__)
    logger.debug(f"Processing taxi ride data from: {input_file}")
    data = pandas.read_parquet(input_file)

    outliers = outlier_detector.detect_outliers(data)
    logger.debug("Detected %s outliers", len(outliers))

    outliers.to_csv(sys.stdout, index=False, sep=",")