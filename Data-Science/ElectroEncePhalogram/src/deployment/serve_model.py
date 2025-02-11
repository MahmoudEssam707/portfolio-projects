from fastapi import FastAPI, Response
from pydantic import BaseModel
import numpy as np
import joblib
import uvicorn
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# Define Prometheus Metrics
prediction_counter = Counter("total_predictions", "Number of predictions", ["label"])

# Load the trained model
model = joblib.load("model.pkl")

# Load the scaler
scaler = joblib.load("scaler.pkl")  

# Mapping prediction values to human-readable labels
LABELS = {0: "open", 1: "closed"}

# Input model for a single sample
class SingleInputData(BaseModel):
    features: list[float]  # A single input sample

# Input model for batch predictions
class BatchInputData(BaseModel):
    features: list[list[float]]  # A list of input samples

@app.get("/")
def read_root():
    return {"message": "Welcome to the EEG Eye State Detection API!"}

@app.post("/predict")
def predict(data: SingleInputData):
    """Predict for a single input sample."""
    input_array = np.array(data.features).reshape(1, -1)  # Reshape to (1, features)
    scaled_array = scaler.transform(input_array)  # Apply scaling
    prediction = model.predict(scaled_array)[0]
    predicted_label = LABELS[int(prediction)]
    prediction_counter.labels(predicted_label).inc() 
    return {"prediction": predicted_label}

# @app.post("/predict_batch")
# def predict_batch(data: BatchInputData):
#     """Predict for a batch of input samples."""
#     input_array = np.array(data.features)  # Convert to NumPy array
#     scaled_array = scaler.transform(input_array)  # Apply scaling
#     predictions = model.predict(scaled_array)
#     return {"predictions": [LABELS[int(pred)] for pred in predictions]}
@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

