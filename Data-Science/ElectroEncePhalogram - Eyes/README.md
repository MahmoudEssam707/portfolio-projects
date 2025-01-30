# EEG Eye State Detection

## Overview
This project involves analyzing EEG data collected from the Emotiv EEG Neuroheadset to determine eye state (open or closed). The dataset consists of continuous EEG measurements over a duration of 117 seconds, with eye state labels added manually based on video frame analysis.

### Eye State Representation
- `1`: Eye Closed
- `0`: Eye Open

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

## Results
| Model | Accuracy | Precision | Recall | F1 Score |
|-----------------|----------|-----------|--------|---------|
| **Best Model: KNN** | **96.26%** | **96.27%** | **96.26%** | **96.26%** |

## Key Takeaways
- EEG signals can be effectively analyzed to determine eye state.
- K-Nearest Neighbors (KNN) provided the best performance.
- Data preprocessing and feature scaling significantly impact model performance.

## Future Improvements
- Experiment with deep learning models (e.g., CNN, LSTMs) for EEG classification.
- Increase dataset size for better generalization.
- Optimize feature selection for improved efficiency.