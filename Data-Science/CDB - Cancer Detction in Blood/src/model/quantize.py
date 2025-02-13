import tensorflow as tf
import numpy as np
import yaml
import os
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import accuracy_score

# Load config
with open("/home/mahmoud/CDIB/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Paths from config.yaml
processed_data_path = config["paths"]["processed_data"]
model_path = os.path.join(config["paths"]["checkpoint_dir"], "CNN_best_v1.keras")
quantized_model_path = os.path.join(config["paths"]["model_dir"], "CNN_best_v1_quantized.tflite")

image_size = tuple(config["training"]["image_size"])
batch_size = config["training"]["batch_size"]

# Load original model
model = tf.keras.models.load_model(model_path)
print("✅ Original Model Loaded")

# Load Test Data
test_df = pd.read_csv(os.path.join(processed_data_path, "test.csv"))
test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)
test_generator = test_datagen.flow_from_dataframe(
    test_df, x_col="Image", y_col="Target",
    target_size=image_size,
    batch_size=1,  # Process one image at a time for TFLite inference
    color_mode="rgb",
    class_mode="categorical",
    shuffle=False
)

# Evaluate Original Model
original_loss, original_acc = model.evaluate(test_generator)
print(f"🎯 Original Model Accuracy: {original_acc:.4f}")

# --- QUANTIZATION ---
def representative_dataset():
    for _ in range(100):
        batch = next(test_generator)[0]  # Get batch images
        yield [batch.astype(np.float32)]

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset
converter.target_spec.supported_types = [tf.float16]  # Float16 Quantization

tflite_model = converter.convert()

# Save Quantized Model
with open(quantized_model_path, "wb") as f:
    f.write(tflite_model)

print(f"✅ Quantized Model Saved at: {quantized_model_path}")

# --- TEST QUANTIZED MODEL ---
# Load Quantized Model
interpreter = tf.lite.Interpreter(model_path=quantized_model_path)
interpreter.allocate_tensors()

# Get Input and Output Tensor Details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Run Inference on Test Data
y_true = []
y_pred = []

for i in range(len(test_generator)):
    image, label = test_generator[i]  
    image = image.astype(np.float32)  

    # Run TFLite Inference
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])  # Get prediction

    # Store True & Predicted Labels
    y_true.append(np.argmax(label, axis=1)[0])  # Convert one-hot to label index
    y_pred.append(np.argmax(output))  # Get predicted class index

# Compute Accuracy
quantized_accuracy = accuracy_score(y_true, y_pred)
print(f"🎯 Quantized Model Accuracy: {quantized_accuracy:.4f}")

# Compare Before & After Quantization
print("\n📊 Model Accuracy Comparison:")
print(f"🔹 Original Model Accuracy:  {original_acc:.8f}")
print(f"🔹 Quantized Model Accuracy: {quantized_accuracy:.8f}")
