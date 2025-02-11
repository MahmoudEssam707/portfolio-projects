import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tabulate import tabulate

# Load data
data_path = '/home/mahmoud/eeg-mlops/data/raw/eeg-headset.csv'
data = pd.read_csv(data_path)
data["eye_state"] = data["eye_state"].replace({1: 0, 2: 1})

# Identify and print outliers
outliers = data[(data > 100000).any(axis=1)]
print("Rows with outliers greater than 100000:")
print(tabulate(outliers, headers='keys', tablefmt='pretty'))

# Remove outliers
data = data[(data < 100000).all(axis=1)]

# Data Loading and Preprocessing
def load_and_preprocess_data(df):
    """Load and preprocess the data"""
    # Separate features and target
    X = df.drop('eye_state', axis=1)
    y = df['eye_state']
    
    # Split data into train, validation, and test sets
    X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
    X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.2, random_state=42, shuffle=True)

    print("Train shape:", X_train.shape, y_train.shape)
    print("Validation shape:", X_val.shape, y_val.shape)
    print("Test shape:", X_test.shape, y_test.shape)

    # Scale features using StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    # Save the trained scaler for use in FastAPI
    joblib.dump(scaler, "/home/mahmoud/eeg-mlops/data/processed/scaler.pkl")
    
    print("Scaler saved as scaler.pkl")
    print("Scaler mean:", scaler.mean_)
    print("Scaler scale:", scaler.scale_)

    return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test

# Apply preprocessing
X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test = load_and_preprocess_data(data)

# Save processed data
np.save('/home/mahmoud/eeg-mlops/data/processed/X_train.npy', X_train_scaled)
np.save('/home/mahmoud/eeg-mlops/data/processed/X_val.npy', X_val_scaled)
np.save('/home/mahmoud/eeg-mlops/data/processed/X_test.npy', X_test_scaled)
np.save('/home/mahmoud/eeg-mlops/data/processed/y_train.npy', y_train)
np.save('/home/mahmoud/eeg-mlops/data/processed/y_val.npy', y_val)
np.save('/home/mahmoud/eeg-mlops/data/processed/y_test.npy', y_test)

print("✅ Data processing complete. Processed files and scaler saved.")
