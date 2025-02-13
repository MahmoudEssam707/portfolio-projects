# Cancer Detection in Blood – Deep Learning Approach

This study applies **Convolutional Neural Networks (CNNs)** to detect leukemia from **microscopic blood cell images**. The process includes **dataset preparation, CNN modeling, training, evaluation, and performance analysis**.

---

## 1. Dataset & Preprocessing  

The dataset consists of **high-resolution microscopic images** categorized into five blood cell types:  

| Blood Cell Type        | Label            |
|------------------------|-----------------|
| Monocyte              | `monocyte`       |
| Basophil              | `basophil`       |
| Erythroblast          | `erythroblast`   |
| Segmented Neutrophil  | `seg_neutrophil` |
| Myeloblast (Critical) | `myeloblast`     |

### Data Preparation  
- Images are **organized into labeled directories**.  
- A **structured format (file paths + labels)** is created.  
- The dataset is **split into training (3500), validation (750), and test (750)**.  
- **Image verification** ensures correct loading.  

### Data Augmentation  
To **enhance generalization**, the following techniques are applied:  

- Rotation and zooming  
- Width and height shifts  
- Horizontal flipping  
- Pixel rescaling  

## Project Structure
```
cancer-detection-blood/
├── data/
│   ├── raw/               # Original image dataset
│   └── processed/         # Preprocessed images
├── src/
│   ├── model/            
│   │   ├── train.py      # Training script
│   │   └── predict.py    # Prediction script
│   └── utils/            # Utility functions
├── notebooks/            # Jupyter notebooks
├── tests/               # Unit tests
├── config.yaml          # Configuration file
└── requirements.txt     # Project dependencies
```
---

## 2. CNN Model Architecture  

A **deep learning model** is designed to classify blood cells accurately.  

### Feature Extraction (Convolutional Layers)
- Multiple **convolutional layers** extract features.  
- **Batch normalization** stabilizes learning.  
- **Max pooling layers** reduce dimensionality.  

### Classification Layers
- Extracted features are **flattened**.  
- Fully **connected layers** process the features.  
- A **softmax activation layer** predicts one of the five blood cell types.  

### Optimization & Training Strategy
- **Adam optimizer** for fast convergence.  
- **Categorical cross-entropy loss** for multi-class classification.  
- **Early stopping** prevents overfitting.  
- **Learning rate reduction** for adaptive training.  

---

## 3. Model Training & Performance  

The model is trained on **3500 images**, validated on **750**, and tested on **750**.  

### Training Progress
- Accuracy starts at **57%** and rapidly improves.  
- Reaches **98.53% test accuracy** in **30 epochs**.  
- **Myeloblast detection (100% recall)** ensures critical cases aren’t missed.  

### Evaluation Metrics
- **Accuracy** – Measures overall classification performance.  
- **Precision & Recall** – Assesses how well each class is detected.  
- **F1-score** – Balances precision and recall.  
- **Confusion Matrix** – Visualizes classification errors.  

---

## 4. Model Performance & Insights  

### Confusion Matrix Findings
- The model performs well across all categories.  
- **100% recall for myeloblasts**, ensuring no high-risk cases are missed.  

### Classification Report Highlights
| Cell Type       | Precision | Recall  | F1-Score |
|----------------|-----------|---------|----------|
| Basophils     | 96.6%     | 94.0%   | 95.3%    |
| Erythroblasts | 97.3%     | 98.0%   | 97.6%    |
| Monocytes     | 96.7%     | 98.7%   | 97.7%    |
| Myeloblasts   | **98.0%** | **100%** | **99.0%** |
| Segmented Neutrophils | 100% | 98.0%  | 99.0%    |

The model ensures **no myeloblast cases are missed**, crucial for early leukemia detection.

## 5. MLOps Integration

### MLflow Tracking
- Experiment tracking with metrics and artifacts
- Model versioning and deployment
- Hyperparameter optimization results

### Model Serving
- FastAPI endpoint for real-time predictions
- Docker containerization
- Load testing results

### Current Release (v1.0)
- [x] MLflow integration
- [x] FastAPI deployment with dockerization
- [x] Web-App for easier actions 
- [x] Vercel deployed service:


---
## 5. Conclusion & Impact

This deep learning project achieved **98.53% accuracy** demonstrating significant potential for automating early leukemia detection in clinical settings, while maintaining perfect recall for critical cases and establishing a robust foundation for future medical AI applications.

---
