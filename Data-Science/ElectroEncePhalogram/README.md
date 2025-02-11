# EEG Eye State Detection

## Overview
This project involves analyzing EEG data collected from the Emotiv EEG Neuroheadset to determine eye state (open or closed). The dataset consists of continuous EEG measurements over a duration of 117 seconds, with eye state labels added manually based on video frame analysis.

### Eye State Representation
- `1`: Eye Closed
- `0`: Eye Open

## Project Structure

```
📂 data
   ├── 📂 raw  # Contains the original EEG dataset "ignored"

📂 src
   ├── 📂 data  # Data loading and preprocessing scripts
   │   ├── dataset.py
   ├── 📂 models  # Model training scripts and saved experiments
   │   ├── train.py
   ├── 📂 deployment  # Deployment-related files
   │   ├── Dockerfile
   │   ├── model.pkl
   │   ├── scaler.pkl
   │   ├── serve_model.py  # API using FastAPI
   │   ├── requirements.txt
   ├── 📂 test  # Unit tests
   │   ├── test.py
   ├── 📂 visualization  # EDA and visualization scripts

.gitignore
requirements.txt -> as a main requirements for whole script
```

## Project Workflow

### 1. Data Overview
- Load EEG dataset.
- Display first few rows.
- Check for missing values or inconsistencies.

### 2. Exploratory Data Analysis (EDA)
- Compute summary statistics.
- Visualize the correlation matrix.
- Identify highly correlated features.
- Detect outliers using boxplots.
- Plot feature distributions.

### 3. Machine Learning Model Pipeline
#### **Data Preparation**
- Features are extracted from EEG signals.
- Data is split into Training (80%), Validation (20%), and Test (20%) sets.
- Standardization is applied using `StandardScaler`.

#### **Model Training and Hyperparameter Tuning**
The following models are trained and optimized using `RandomizedSearchCV`:
- Extra Trees
- AdaBoost
- Gradient Boosting
- Random Forest
- Support Vector Classifier (SVC)
- K-Nearest Neighbors (KNN)
- Decision Tree
- Multi-layer Perceptron (MLP)
- XGBoost
- LightGBM

#### **Model Evaluation**
Metrics used for evaluation:
- **Accuracy**
- **Precision**
- **Recall**
- **F1 Score**
- **Confusion Matrix**

The best model is selected based on the highest F1 score.

### 4. Model Testing
- The selected model is tested on unseen data.
- Performance is evaluated using the same metrics.
- A confusion matrix is plotted.

### 5. Random EEG Sample Prediction Simulation
- Random samples from the dataset are selected.
- Their eye state is predicted using the trained model.
- Results are compared with actual labels.

## API Deployment
The trained model is deployed using **FastAPI**.
### API Endpoints
- **GET `/`** → Welcome message.
- **POST `/predict`** → Predicts eye state for a single input sample.
- **POST `/predict_batch`** → Predicts eye state for multiple input samples.

The API loads the trained model (`model.pkl`) and applies the corresponding scaler (`scaler.pkl`) before making predictions.

## Results
| Model | Accuracy | Precision | Recall | F1 Score |
|-----------------|----------|-----------|--------|---------|
| **Best Model: KNN** | **96.26%** | **96.27%** | **96.26%** | **96.26%** |

## Key Takeaways
- EEG signals can be effectively analyzed to determine eye state.
- K-Nearest Neighbors (KNN) provided the best performance.
- Data preprocessing and feature scaling significantly impact model performance.

## Deployment Strategy
- Containerized using **Docker** (`Dockerfile` included).
- Deployed using **Railway** at: [https://eeg-humachine.up.railway.app/](https://eeg-humachine.up.railway.app/)
- Future deployment plans include migrating to **AWS, Azure, or GCP** for better scalability and reliability.
- Implemented monitoring using **Prometheus**, exposing metrics at `/metrics`.
- Model is served using **FastAPI**, allowing real-time predictions via simple API calls.
- Example API test:

```bash
curl -X 'POST' 'https://eeg-humachine.up.railway.app/predict' \
     -H 'Content-Type: application/json' \
     -d '{
           "features": [4285.64, 4004.62, 4264.1, 4115.38, 4320.0, 4615.9, 4071.79, 4608.72, 4201.03, 4224.62, 4162.56, 4271.79, 4584.1, 4352.31]
         }'
```

You can try testing it with your own data!

