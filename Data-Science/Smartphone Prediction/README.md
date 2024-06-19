# Smartphone Prediction Analysis

## Table of Contents
1. [Introduction](#introduction)
2. [Data Cleaning and Wrangling](#data-cleaning-and-wrangling)
3. [Exploratory Data Analysis](#exploratory-data-analysis)
4. [Model Building](#model-building)
5. [Model Evaluation](#model-evaluation)
6. [Conclusion](#conclusion)

## Introduction <a name="introduction"></a>

This Markdown document summarizes the analysis and modeling of smartphone data. The analysis includes data cleaning, exploratory data analysis (EDA), and building machine learning models to predict smartphone prices based on various features.

## Data Cleaning and Wrangling <a name="data-cleaning-and-wrangling"></a>

The dataset undergoes several cleaning steps to handle missing values and prepare it for analysis:
- NaN values are filled using backward and forward filling methods.
- Statistical summaries are generated to understand the cleaned data.

## Exploratory Data Analysis <a name="exploratory-data-analysis"></a>

### Average Price of Smartphone Brands
- Visualizes the average price of different smartphone brands using a bar chart.

### Price Distribution
- Checks the distribution of smartphone prices using a histogram.
- Applies Box-Cox transformation to normalize the price distribution.

### Processor Speed and Cores Analysis
- Analyzes average processor speed and number of cores across different smartphone brands using bar charts.

### RAM Capacity Analysis
- Examines the average RAM capacity of smartphone brands using a bar chart.

## Model Building <a name="model-building"></a>

### Data Preparation
- Splits the data into training, validation, and test sets.
- Scales the features using StandardScaler.

### Model Training
- Implements several regression models:
  - Linear Regression
  - Ridge Regression with hyperparameter tuning
  - Lasso Regression with hyperparameter tuning
  - Random Forest Regressor with hyperparameter tuning
  - XGBoost Regressor with hyperparameter tuning

## Model Evaluation <a name="model-evaluation"></a>

- Evaluates models based on Mean Squared Error (MSE) on the validation set:
  - **Linear Regression:** MSE = 0.0007
  - **Ridge Regression:** MSE = 0.0007
  - **Lasso Regression:** MSE = 0.0018
  - **Random Forest Regressor:** MSE = 0.0007 **Best One**
  - **XGBoost Regressor:** MSE = 0.0008

## Conclusion <a name="conclusion"></a>

This analysis provides insights into smartphone pricing trends and demonstrates the effectiveness of various machine learning models in predicting smartphone prices based on their features.

