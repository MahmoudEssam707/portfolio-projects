import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import yaml
from tqdm import tqdm

# Load config.yaml
with open("/home/mahmoud/CDIB/config.yaml", "r") as file:
    config = yaml.safe_load(file)

PROCESSED_DATA_PATH = config["paths"]["processed_data"]
IMAGE_SIZE = tuple(config["training"]["image_size"])
LABELS = ['basophil', 'erythroblast', 'monocyte', 'myeloblast', 'seg_neutrophil']

# Load dataset
df = pd.read_csv(os.path.join(PROCESSED_DATA_PATH, "dataset.csv"))

# Visualize class distribution
def plot_class_distribution(df):
    plt.figure(figsize=(8, 5))
    sns.countplot(x=df['Target'], order=LABELS, palette="viridis")
    plt.title("Class Distribution")
    plt.xlabel("Cell Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()

# Display sample images
def show_sample_images(df, num_samples=5):
    fig, axes = plt.subplots(len(LABELS), num_samples, figsize=(num_samples * 2, len(LABELS) * 2))
    for i, label in enumerate(LABELS):
        sample_paths = df[df['Target'] == label]['Image'].sample(num_samples, random_state=42).values
        for j, img_path in enumerate(sample_paths):
            img = cv2.imread(img_path)
            img = cv2.resize(img, IMAGE_SIZE)
            axes[i, j].imshow(img)
            axes[i, j].axis('off')
            if j == 0:
                axes[i, j].set_title(label, fontsize=12)
    plt.tight_layout()
    plt.show()

# Check image dimensions
def check_image_properties(df):
    sizes = []
    for img_path in tqdm(df['Image'], desc="Checking image properties"):
        img = cv2.imread(img_path)
        sizes.append(img.shape if img is not None else (0, 0))
    sizes = np.array(sizes)
    print(f"Unique image sizes: {np.unique(sizes, axis=0)}")
    
    plt.figure(figsize=(8, 5))
    plt.scatter(sizes[:, 1], sizes[:, 0], alpha=0.5, color='blue')
    plt.xlabel("Width")
    plt.ylabel("Height")
    plt.title("Image Size Distribution")
    plt.show()

if __name__ == "__main__":
    print("Performing EDA...")
    plot_class_distribution(df)
    show_sample_images(df)
    check_image_properties(df)
    print("EDA Completed!")
