import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier,
    AdaBoostClassifier, ExtraTreesClassifier
)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

def load_data():
    """Load preprocessed data"""
    X_train = np.load('/home/mahmoud/eeg-mlops/data/processed/X_train.npy')
    X_val = np.load('/home/mahmoud/eeg-mlops/data/processed/X_val.npy')
    X_test = np.load('/home/mahmoud/eeg-mlops/data/processed/X_test.npy')
    y_train = np.load('/home/mahmoud/eeg-mlops/data/processed/y_train.npy')
    y_val = np.load('/home/mahmoud/eeg-mlops/data/processed/y_val.npy')
    y_test = np.load('/home/mahmoud/eeg-mlops/data/processed/y_test.npy')
    return X_train, X_val, X_test, y_train, y_val, y_test


# Function to Evaluate Metrics
def evaluate_metrics(y_true, y_pred):
    """Calculate accuracy, precision, recall, and F1-score"""
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted'),
        'recall': recall_score(y_true, y_pred, average='weighted'),
        'f1_score': f1_score(y_true, y_pred, average='weighted')
    }
    return metrics

# Function to Plot Confusion Matrix
def plot_confusion_matrix(y_true, y_pred, title):
    """Plot confusion matrix and save it as an artifact"""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['open', 'closed'], yticklabels=['open', 'closed'])
    plt.title(f'Confusion Matrix - {title}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    cm_filename = f'confusion_matrix_{title}.png'
    plt.savefig(cm_filename)
    plt.close()
    return cm_filename

# Function to Train Models and Log to MLflow
def train_models():
    """Train multiple models and log results in MLflow"""
    mlflow.set_experiment("eeg_eye_state_detection")
    # Load Data
    X_train, X_val, X_test, y_train, y_val, y_test = load_data()
    # Define models with their hyperparameters
    models_params = {
        "Extra Trees": (ExtraTreesClassifier(), {
            "n_estimators": [100, 200, 300, 500],
            "max_depth": [None, 10, 20, 30],
            "min_samples_split": [2, 5, 10],
            "max_features": ["sqrt", "log2", None],
            "bootstrap": [True, False]
        }),
        "AdaBoost": (AdaBoostClassifier(), {
            "n_estimators": [50, 100, 200],
            "learning_rate": [0.01, 0.1, 0.5, 1.0],
            "algorithm": ['SAMME', 'SAMME.R']
        }),
        "Gradient Boosting": (GradientBoostingClassifier(), {
            "n_estimators": [100, 200, 300],
            "learning_rate": [0.01, 0.1, 0.3],
            "max_depth": [3, 5, 7],
            "min_samples_split": [2, 5, 10],
            "subsample": [0.8, 0.9, 1.0]
        }),
        "Random Forest": (RandomForestClassifier(), {
            "n_estimators": [100, 200, 500],
            "max_depth": [None, 10, 20, 30],
            "min_samples_split": [2, 5, 10],
            "max_features": ["sqrt", "log2", None],
            "bootstrap": [True, False]
        }),
        "Support Vector Classifier": (SVC(), {
            "C": [0.1, 1, 10],
            "kernel": ['linear', 'rbf'],
            "gamma": ['scale', 'auto']
        }),
        "K-Nearest Neighbors": (KNeighborsClassifier(), {
            "n_neighbors": [3, 5, 7],
            "weights": ['uniform', 'distance'],
            "algorithm": ['auto', 'kd_tree', 'brute']
        }),
        "Decision Tree": (DecisionTreeClassifier(), {
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5, 10],
            "criterion": ['gini', 'entropy']
        }),
        "MLP Classifier": (MLPClassifier(), {
            "hidden_layer_sizes": [(50,), (100,), (50, 50)],
            "activation": ['relu', 'tanh', 'logistic'],
            "solver": ['adam', 'sgd'],
            "max_iter": [200, 300]
        }),
        "XGBoost": (xgb.XGBClassifier(), {
            "n_estimators": [100, 200, 300],
            "learning_rate": [0.01, 0.1, 0.3],
            "max_depth": [3, 5, 7],
            "subsample": [0.8, 0.9, 1.0],
            "colsample_bytree": [0.7, 0.8, 0.9]
        }),
}
    best_models = {}
    all_metrics = {}

    # Train and Evaluate Models
    for name, (model, params) in models_params.items():
        with mlflow.start_run(run_name=name):
            print(f"\nTraining {name}...")

            # Perform RandomizedSearchCV
            search = RandomizedSearchCV(
                model, params, n_iter=10, cv=3,
                scoring="accuracy", n_jobs=-1,
                verbose=1, random_state=42
            )

            # Train model
            search.fit(X_train, y_train)

            # Get Predictions
            y_val_pred = search.best_estimator_.predict(X_val)

            # Calculate Metrics
            metrics = evaluate_metrics(y_val, y_val_pred)

            # Log Best Parameters & Metrics
            mlflow.log_params(search.best_params_)
            mlflow.log_metrics(metrics)

            # Log Confusion Matrix as Artifact
            cm_filename = plot_confusion_matrix(y_val, y_val_pred, name)
            mlflow.log_artifact(cm_filename)

            # Save Best Model
            best_models[name] = search.best_estimator_
            all_metrics[name] = metrics

            # Log Model
            input_example = X_val[:5]  # A small batch of inputs as an example
            mlflow.sklearn.log_model(search.best_estimator_, name, input_example=input_example)


            print(f"\nBest parameters for {name}: {search.best_params_}")
            print("Validation Metrics:")
            for metric_name, value in metrics.items():
                print(f"{metric_name}: {value:.4f}")

    # Find Best Model Based on F1-score
    best_model_name = max(all_metrics, key=lambda x: all_metrics[x]['f1_score'])
    best_model = best_models[best_model_name]

    # Evaluate Best Model on Test Set
    with mlflow.start_run(run_name=f"{best_model_name}_test_evaluation"):
        test_metrics = evaluate_metrics(y_test, best_model.predict(X_test))
        mlflow.log_metrics({f"test_{k}": v for k, v in test_metrics.items()})
        
        input_example = X_test[:5]
        model = mlflow.sklearn.log_model(best_model, best_model_name, input_example=input_example)
        
        # Log Confusion Matrix
        mlflow.log_artifact(plot_confusion_matrix(y_test, best_model.predict(X_test), "test"))

        #Register Best Model in MLflow Model Registry
        registered_model = mlflow.register_model(model.model_uri, "EEG_Eye_State_Model")
        print(f"\n✅ Best performing model: {best_model_name}")
        print(f"🔹 Model Registered as: {registered_model.name}")

    return best_model_name, best_model

if __name__ == "__main__":
    print("Starting model training pipeline...")
    best_model_name, best_model = train_models()
    print(f"\nBest performing model: {best_model_name}")
