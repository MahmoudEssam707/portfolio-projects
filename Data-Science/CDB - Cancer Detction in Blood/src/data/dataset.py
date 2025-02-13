import os
import pandas as pd
import yaml
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")
# Load config.yaml
with open("/home/mahmoud/CDIB/config.yaml", "r") as file:
    config = yaml.safe_load(file)

RAW_DATA_PATH = config["paths"]["raw_data"]
PROCESSED_DATA_PATH = config["paths"]["processed_data"]
IMAGE_SIZE = tuple(config["training"]["image_size"])

# Blood cell categories
LABELS = ['basophil', 'erythroblast', 'monocyte', 'myeloblast', 'seg_neutrophil']

def load_and_process_images():
    """
    Load images from raw data, preprocess them, and save them for training.
    """
    data = []
    
    for label in LABELS:
        folder_path = os.path.join(RAW_DATA_PATH, label)
        for filename in tqdm(os.listdir(folder_path), desc=f"Processing {label}"):
            img_path = os.path.join(folder_path, filename)
            data.append({'Image': img_path, 'Target': label})
    
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(PROCESSED_DATA_PATH, "dataset.csv"), index=False)
    print("Dataset saved successfully!")
    return df

# Split dataset
def split_dataset(df):
    """
    Split dataset into train, validation, and test sets.
    """
    train_df, temp_df = train_test_split(df, train_size=0.9, random_state=42, stratify=df['Target'],shuffle=True) # 4500 trainable images
    val_df, test_df = train_test_split(temp_df, train_size=0.5, random_state=42, stratify=temp_df['Target'],shuffle=True) # 250 validation and 250 test images
    # Shape of data now
    print(f"Train shape: {train_df.shape}, Validation shape: {val_df.shape}, Test shape: {test_df.shape}")
    train_df.to_csv(os.path.join(PROCESSED_DATA_PATH, "train.csv"), index=False)
    val_df.to_csv(os.path.join(PROCESSED_DATA_PATH, "val.csv"), index=False)
    test_df.to_csv(os.path.join(PROCESSED_DATA_PATH, "test.csv"), index=False)
    
    print("Data split into train, validation, and test sets!")
    return train_df, val_df, test_df

if __name__ == "__main__":
    df = load_and_process_images()
    train_df, val_df, test_df = split_dataset(df)
