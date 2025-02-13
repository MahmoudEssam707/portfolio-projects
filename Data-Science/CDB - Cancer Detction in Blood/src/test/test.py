import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load config.yaml
with open("/home/mahmoud/CDIB/config.yaml", "r") as file:
    config = yaml.safe_load(file)

PROCESSED_DATA_PATH = config["paths"]["processed_data"]
CHECKPOINTS_PATH = config["paths"]["checkpoint_dir"]
IMAGE_SIZE = tuple(config["training"]["image_size"])
BATCH_SIZE = config["training"]["batch_size"]

# Load test dataset
test_df = pd.read_csv(os.path.join(PROCESSED_DATA_PATH, "test.csv"))

def create_test_generator(df):
    test_datagen = ImageDataGenerator(rescale=1./255)
    return test_datagen.flow_from_dataframe(
        df, x_col="Image", y_col="Target", target_size=IMAGE_SIZE, batch_size=BATCH_SIZE, 
        class_mode='categorical', color_mode='rgb', shuffle=False
    )

# Load test data generator
test_generator = create_test_generator(test_df)

# Load best model from MLflow 
best_model = load_model(os.path.join(CHECKPOINTS_PATH, "CNN_best_v1.keras"))

# Get true labels
y_true = test_generator.classes
class_labels = list(test_generator.class_indices.keys())

# Get predictions and confidence scores
predictions = best_model.predict(test_generator)
y_pred = np.argmax(predictions, axis=1)
confidence_scores = np.max(predictions, axis=1) * 100  

def plot_sample_predictions(test_generator, model, num_images=9):
    # Load all images and labels from the generator
    test_images, test_labels = next(test_generator)
    
    # Randomly select indices
    indices = random.sample(range(len(test_images)), min(num_images, len(test_images)))
    
    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    for i, ax in enumerate(axes.flat):
        if i >= len(indices):
            break
        idx = indices[i]
        img = test_images[idx]
        true_label = np.argmax(test_labels[idx])  # Convert one-hot encoding to class index
        
        # Make a prediction
        pred_probs = model.predict(img[np.newaxis, ...])[0]  # Add batch dimension
        pred_label = np.argmax(pred_probs)
        confidence = np.max(pred_probs) * 100  # Confidence percentage
        
        # Set title color based on correctness
        color = 'green' if true_label == pred_label else 'red'
        
        ax.imshow(img)
        ax.set_title(f"True: {class_labels[true_label]}\nPred: {class_labels[pred_label]}\nConf: {confidence:.2f}%", color=color)
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()

plot_sample_predictions(test_generator, best_model)

# Plot confusion matrix
def plot_confusion_matrix(y_true, y_pred, class_labels):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_labels, yticklabels=class_labels)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.show()

plot_confusion_matrix(y_true, y_pred, class_labels)

# Print classification metrics with confidence scores
print("Classification Report with Confidence Scores:")
report = classification_report(y_true, y_pred, target_names=class_labels, output_dict=True, zero_division=0)
for label, metrics in report.items():
    if label in class_labels:  # Exclude averages
        print(f"\nClass: {label}")
        print(f"Precision: {metrics['precision']:.2f}, Recall: {metrics['recall']:.2f}, F1-score: {metrics['f1-score']:.2f}")

