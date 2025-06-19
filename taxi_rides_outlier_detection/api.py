from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

class OutlierDetectionRequest(BaseModel):
    ride_time: float
    trip_distance: float

class OutlierDetectionResponse(BaseModel):
    outlier: bool

@app.get("/detect-outliers", response_model=OutlierDetectionResponse)
def forecast_sales(
    ride_time: float = Query(..., description="Ride time in seconds"),
    trip_distance: float = Query(..., description="Trip distance in miles")
):    
    import mlflow
    model_uri = "models:/taxi-ride-outlier-detection-model/latest"
    try:
        import mlflow.pyfunc
        model = mlflow.pyfunc.load_model(model_uri)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model loading failed: {str(e)}")
    
    # Prepare input DataFrame for the model
    input_df = pd.DataFrame([{
        "ride_time": ride_time,
        "trip_distance": trip_distance
    }])

    # Predict using the loaded model
    try:
        preds = model.predict(input_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # Assume the model returns a boolean or 0/1 for outlier detection
    outlier = bool(preds[0]) if hasattr(preds, '__getitem__') else bool(preds)

    return OutlierDetectionResponse(outlier=outlier)