from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

def train_random_forest_classifier(labeled_taxi_rides_data: pd.DataFrame) -> tuple[RandomForestClassifier, dict]:
    # Features and target
    X = labeled_taxi_rides_data[['ride_time', 'trip_distance']]
    y = labeled_taxi_rides_data['outlier']

    # Split data for training and testing
    # As the dataset is imbalanced, stratify=y will ensure that the split maintains the proportion of classes
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Use class_weight='balanced' to handle class imbalance
    clf = RandomForestClassifier(class_weight='balanced', random_state=42)
    clf.fit(X_train, y_train)

    # Predict on test set
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred, digits=4, output_dict=True)

    return (clf, report)

def detect_outliers(taxi_rides_data: pd.DataFrame, model: RandomForestClassifier) -> pd.DataFrame:
    raw_data = taxi_rides_data

    data = pd.DataFrame()
    raw_data['tpep_pickup_datetime'] = pd.to_datetime(raw_data['tpep_pickup_datetime'])
    raw_data['tpep_dropoff_datetime'] = pd.to_datetime(raw_data['tpep_dropoff_datetime'])
    data['ride_time'] = (raw_data['tpep_dropoff_datetime'] - raw_data['tpep_pickup_datetime']).dt.total_seconds()
    data['date'] = raw_data['tpep_pickup_datetime'].dt.date
    data['ride_id'] = raw_data.index
    data['trip_distance'] = raw_data['trip_distance']

    # Features for prediction
    X = data[['ride_time', 'trip_distance']]
    
    # Predict outliers
    data['outlier'] = model.predict(X)
    
    # Return only the rows classified as outliers
    return data[data['outlier'] == 1]
