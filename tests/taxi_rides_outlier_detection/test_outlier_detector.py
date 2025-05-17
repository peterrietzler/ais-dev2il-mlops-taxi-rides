from taxi_rides_outlier_detection.outlier_detector import detect_outliers
from test_fixtures import taxi_rides_test_data

def test_detect_outliers(taxi_rides_test_data): 
    outliers, metadata = detect_outliers(taxi_rides_test_data)
    assert len(outliers) == 20
    assert outliers.columns.tolist() == ['ride_dist', 'ride_time', 'date', 'ride_id']

# TODO - add test for CLI app 
