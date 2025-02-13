import base64
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import uvicorn

IMAGE_SIZE = [128, 128]
MODEL_PATH = "CNN_best_v1_quantized.tflite"  
app = FastAPI(title="Cancer Detection API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

templates = Jinja2Templates(directory="templates")

# Load quantized TFLite model
try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()

    # Get model input/output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    class_names = ["Erythroblast", "Basophil", "Monocyte", "Myeloblast", "Seg-Neutrophil"]
except Exception as e:
    raise RuntimeError(f"Failed to load quantized model: {e}")

async def preprocess_image(image_data: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_data)).convert("RGB").resize(IMAGE_SIZE)
    img_array = np.expand_dims(np.array(image) / 255.0, axis=0)
    return img_array

def run_inference(image: np.ndarray) -> np.ndarray:
    # Set the input tensor for TFLite model
    interpreter.set_tensor(input_details[0]['index'], image.astype(np.float32))

    # Run inference
    interpreter.invoke()

    # Get the output from the model
    output = interpreter.get_tensor(output_details[0]['index'])
    return output

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read and preprocess the image
        image_data = await file.read()
        processed_image = await preprocess_image(image_data)

        # Run inference on quantized model
        predictions = run_inference(processed_image)[0]
        
        # Get the predicted class
        predicted_class = np.argmax(predictions)
        confidence = float(predictions[predicted_class])

        # Convert image to base64 for display
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        return {
            "class": class_names[predicted_class],
            "confidence": f"{confidence:.2%}",
            "all_predictions": {
                class_name: f"{float(pred):.2%}"
                for class_name, pred in zip(class_names, predictions)
            },
            "image": encoded_image
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
