FROM python:3.13-slim

WORKDIR /app

COPY taxi_rides_outlier_detection /app/taxi_rides_outlier_detection
COPY pyproject.toml /app

RUN pip install .

ENTRYPOINT [ "detect-taxi-ride-outliers" ]