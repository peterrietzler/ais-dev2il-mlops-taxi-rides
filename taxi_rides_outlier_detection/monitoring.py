import pandas as pd
import datetime

from evidently import Report
from evidently.presets import DataDriftPreset

def detect_drift(reference_data: pd.DataFrame, current_data: pd.DataFrame, date: datetime) -> Report:
    report = Report([
        DataDriftPreset(drift_share=0.25)
    ], include_tests=True)
    
    current_data = current_data.copy()
    current_data['tpep_pickup_datetime'] = pd.to_datetime(current_data['tpep_pickup_datetime'])
    current_data['tpep_dropoff_datetime'] = pd.to_datetime(current_data['tpep_dropoff_datetime'])
    current_data['ride_time'] = (current_data['tpep_dropoff_datetime'] - current_data['tpep_pickup_datetime']).dt.total_seconds()
    
    result = report.run(reference_data=reference_data, current_data=current_data, timestamp=date)
    return result