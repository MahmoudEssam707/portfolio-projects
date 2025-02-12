import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# Load dataset
data = pd.read_csv("your_dataset.csv")  # Change this to your actual dataset file

# 1. Plot Correlation Matrix
def plot_correlation_matrix(data):
    """Plot the correlation matrix heatmap."""
    corr_matrix = data.corr()
    plt.figure(figsize=(20, 10))
    sns.heatmap(corr_matrix, annot=True, xticklabels=corr_matrix.columns, yticklabels=corr_matrix.columns)
    plt.title("Correlation Matrix")
    plt.show()

    # Identify highly correlated features (absolute correlation > 0.7)
    correlated_features = set()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > 0.7:
                colname = corr_matrix.columns[i]
                correlated_features.add((colname, corr_matrix.columns[j], corr_matrix.iloc[i, j]))

    print("Features with correlation greater than 0.7:")
    print(tabulate(correlated_features, headers=['Feature 1', 'Feature 2', 'Correlation'], tablefmt='pretty'))

# 2. Boxplot to check for outliers
def plot_boxplot(data):
    """Plot a boxplot to check for outliers."""
    plt.figure(figsize=(20, 10))
    sns.boxplot(data=data)
    plt.xticks(rotation=90)
    plt.title("Boxplot of Features")
    plt.show()

# 3. Identify & remove extreme outliers (>100000)
def detect_outliers(data, threshold=100000):
    """Identify and remove extreme outliers."""
    outliers = data[(data > threshold).any(axis=1)]
    print("Rows with outliers greater than 100000:")    
    print(tabulate(outliers, headers='keys', tablefmt='pretty'))
    
    # Remove rows with extreme outliers
    clean_data = data[(data < threshold).all(axis=1)]
    return clean_data

# 4. Plot Feature Distributions
def plot_feature_distributions(data):
    """Plot the distribution of all features in a single plot."""
    plt.figure(figsize=(20, 10))
    for column in data.columns:
        sns.kdeplot(data[column], label=column)
    plt.xlim(0, 7000)
    plt.xlabel("Combined Features")
    plt.ylabel("Density")
    plt.legend()
    plt.title("Feature Distributions")
    plt.show()

# Run EDA steps
print("Summary Statistics:")
print(tabulate(data.describe(), headers='keys', tablefmt='pretty'))

plot_correlation_matrix(data)
plot_boxplot(data)

# Detect and remove outliers
data = detect_outliers(data)

# Plot feature distributions
plot_feature_distributions(data)

# Save the cleaned data
data.to_csv("cleaned_dataset.csv", index=False)
print("Cleaned dataset saved as 'cleaned_dataset.csv'")
