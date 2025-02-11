from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import uvicorn

app = FastAPI()

# Load the trained model
model = joblib.load("model.pkl")

# Load the scaler
scaler = joblib.load("scaler.pkl")  # Make sure scaler is saved as 'scaler.pkl'

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
    return {"prediction": LABELS[int(prediction)]}

@app.post("/predict_batch")
def predict_batch(data: BatchInputData):
    """Predict for a batch of input samples."""
    input_array = np.array(data.features)  # Convert to NumPy array
    scaled_array = scaler.transform(input_array)  # Apply scaling
    predictions = model.predict(scaled_array)
    return {"predictions": [LABELS[int(pred)] for pred in predictions]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
