# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, median_absolute_error, explained_variance_score
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.exceptions import ConvergenceWarning
import warnings
warnings.filterwarnings("ignore", category=ConvergenceWarning)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.inspection import permutation_importance
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
import config
import logging
from sklearn.utils.class_weight import compute_class_weight
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_validate
import os
import sys

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

# Load and prepare data
def load_data(file_path, target_variable):
    """
    Load dataset from CSV file and split into training and testing sets.
    
    Parameters:
    file_path (str): Path to the CSV file.
    target_variable (str): Name of the target variable.
    
    Returns:
    tuple: X_train, X_test, y_train, y_test
    """
    try:
        # Load the dataset from the CSV file
        df = pd.read_csv(file_path)
        
        # Split the dataset into features (X) and target (y)
        X = df.drop(target_variable, axis=1)
        y = df[target_variable]
        
        # Handle missing values by replacing them with the mean
        X.fillna(X.mean(), inplace=True)
        y.fillna(y.mean(), inplace=True)
        
        # Split the dataset into training and testing sets
        return train_test_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        # Log any errors that occur during data loading
        logging.error("Error loading data: {}".format(str(e)))
        sys.exit(1)

# Data preprocessing pipeline
def create_pipeline(numeric_features, categorical_features):
    """
    Create a data preprocessing pipeline with feature scaling and selection.
    
    Parameters:
    numeric_features (list): List of numeric feature names.
    categorical_features (list): List of categorical feature names.
    
    Returns:
    Pipeline: Data preprocessing pipeline
    """
    # Create a numeric transformer pipeline
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),  # Replace missing values with the median
        ('scaler', StandardScaler())])  # Scale numeric features
    
    # Create a categorical transformer pipeline
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),  # Replace missing values with a constant
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])  # One-hot encode categorical features
    
    # Create a preprocessor pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])
    
    # Create a pipeline with the preprocessor and a feature selector
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('selector', SelectKBest(f_regression, k=5))])  # Select the top 5 features based on the F-regression score
    
    return pipeline


# Create and train models
def train_models(X_train, y_train, pipeline):
    """
    Create and train linear regression, random forest, and gradient boosting models.
    
    Parameters:
    X_train (DataFrame): Training features.
    y_train (Series): Training target.
    pipeline (Pipeline): Data preprocessing pipeline.
    
    Returns:
    tuple: Trained linear regression, random forest, and gradient boosting models
    """
    # Create a linear regression model pipeline
    lr_model = Pipeline([
        ('preprocessing', pipeline),
        ('lr', LinearRegression())])
    
    # Create a random forest regressor model pipeline
    rf_model = Pipeline([
        ('preprocessing', pipeline),
        ('rf', RandomForestRegressor(n_estimators=100))])
    
    # Create a gradient boosting regressor model pipeline
        gb_model = Pipeline([
        ('preprocessing', pipeline),
        ('gb', GradientBoostingRegressor(n_estimators=100))])
    
    # Create an Elastic Net regressor model pipeline
    en_model = Pipeline([
        ('preprocessing', pipeline),
        ('en', ElasticNet())])
    
    # Train the models
    lr_model.fit(X_train, y_train)
    rf_model.fit(X_train, y_train)
    gb_model.fit(X_train, y_train)
    en_model.fit(X_train, y_train)
    
    return lr_model, rf_model, gb_model, en_model

# Hyperparameter tuning
def tune_hyperparameters(lr_model, rf_model, gb_model, en_model, X_train, y_train):
    """
    Perform hyperparameter tuning using GridSearchCV.
    
    Parameters:
    lr_model (Pipeline): Linear regression model pipeline.
    rf_model (Pipeline): Random forest regressor model pipeline.
    gb_model (Pipeline): Gradient boosting regressor model pipeline.
    en_model (Pipeline): Elastic Net regressor model pipeline.
    X_train (DataFrame): Training features.
    y_train (Series): Training target.
    
    Returns:
    tuple: Tuned linear regression, random forest, and gradient boosting models
    """
    # Define hyperparameter grids for each model
    param_grid_lr = {'lr__C': [0.1, 1, 10]}
    param_grid_rf = {'rf__n_estimators': [50, 100, 200], 'rf__max_depth': [5, 10, 15]}
    param_grid_gb = {'gb__n_estimators': [50, 100, 200], 'gb__learning_rate': [0.1, 0.5, 1]}
    param_grid_en = {'en__alpha': [0.1, 1, 10], 'en__l1_ratio': [0.2, 0.5, 0.8]}
    
    # Perform hyperparameter tuning using GridSearchCV
    grid_search_lr = GridSearchCV(lr_model, param_grid_lr, cv=5)
    grid_search_rf = GridSearchCV(rf_model, param_grid_rf, cv=5)
    grid_search_gb = GridSearchCV(gb_model, param_grid_gb, cv=5)
    grid_search_en = GridSearchCV(en_model, param_grid_en, cv=5)
    
    # Fit the grid searches
    grid_search_lr.fit(X_train, y_train)
    grid_search_rf.fit(X_train, y_train)
    grid_search_gb.fit(X_train, y_train)
    grid_search_en.fit(X_train, y_train)
    
    return grid_search_lr, grid_search_rf, grid_search_gb, grid_search_en


# Evaluate models
def evaluate_models(grid_search_lr, grid_search_rf, grid_search_gb, grid_search_en, X_test, y_test):
    """
    Evaluate model performance using various metrics.
    
    Parameters:
    grid_search_lr (GridSearchCV): Tuned linear regression model.
    grid_search_rf (GridSearchCV): Tuned random forest regressor model.
    grid_search_gb (GridSearchCV): Tuned gradient boosting regressor model.
    grid_search_en (GridSearchCV): Tuned Elastic Net regressor model.
    X_test (DataFrame): Testing features.
    y_test (Series): Testing target.
    """
    # Predict on the test set
    lr_y_pred = grid_search_lr.predict(X_test)
    rf_y_pred = grid_search_rf.predict(X_test)
    gb_y_pred = grid_search_gb.predict(X_test)
    en_y_pred = grid_search_en.predict(X_test)
    
    # Calculate evaluation metrics
    lr_mse = mean_squared_error(y_test, lr_y_pred)
    lr_r2 = r2_score(y_test, lr_y_pred)
    lr_mae = mean_absolute_error(y_test, lr_y_pred)
    lr_medae = median_absolute_error(y_test, lr_y_pred)
    lr_ev = explained_variance_score(y_test, lr_y_pred)
    
    rf_mse = mean_squared_error(y_test, rf_y_pred)
    rf_r2 = r2_score(y_test, rf_y_pred)
    rf_mae = mean_absolute_error(y_test, rf_y_pred)
    rf_medae = median_absolute_error(y_test, rf_y_pred)
    rf_ev = explained_variance_score(y_test, rf_y_pred)
    
    gb_mse = mean_squared_error(y_test, gb_y_pred)
    gb_r2 = r2_score(y_test, gb_y_pred)
    gb_mae = mean_absolute_error(y_test, gb_y_pred)
    gb_medae = median_absolute_error(y_test, gb_y_pred)
    gb_ev = explained_variance_score(y_test, gb_y_pred)
    
    en_mae = mean_absolute_error(y_test, en_y_pred)
    en_medae = median_absolute_error(y_test, en_y_pred)
    en_ev = explained_variance_score(y_test, en_y_pred)
    
    # Print evaluation metrics
        print("Linear Regression:")
    print(f"MSE: {lr_mse:.2f}, R2: {lr_r2:.2f}, MAE: {lr_mae:.2f}, MedAE: {lr_medae:.2f}, EV: {lr_ev:.2f}")
    print("Random Forest Regressor:")
    print(f"MSE: {rf_mse:.2f}, R2: {rf_r2:.2f}, MAE: {rf_mae:.2f}, MedAE: {rf_medae:.2f}, EV: {rf_ev:.2f}")
    print("Gradient Boosting Regressor:")
    print(f"MSE: {gb_mse:.2f}, R2: {gb_r2:.2f}, MAE: {gb_mae:.2f}, MedAE: {gb_medae:.2f}, EV: {gb_ev:.2f}")
    print("Elastic Net Regressor:")
    print(f"MAE: {en_mae:.2f}, MedAE: {en_medae:.2f}, EV: {en_ev:.2f}")


# Visualize results
def visualize_results(grid_search_lr, grid_search_rf, grid_search_gb, grid_search_en, X_test, y_test):
    """
    Visualize model performance using scatter plots and feature importance.
    
    Parameters:
    grid_search_lr (GridSearchCV): Tuned linear regression model.
    grid_search_rf (GridSearchCV): Tuned random forest regressor model.
    grid_search_gb (GridSearchCV): Tuned gradient boosting regressor model.
    grid_search_en (GridSearchCV): Tuned Elastic Net regressor model.
    X_test (DataFrame): Testing features.
    y_test (Series): Testing target.
    """
    # Predict on the test set
    lr_y_pred = grid_search_lr.predict(X_test)
    rf_y_pred = grid_search_rf.predict(X_test)
    gb_y_pred = grid_search_gb.predict(X_test)
    en_y_pred = grid_search_en.predict(X_test)
    
    # Plot scatter plots of predicted vs actual values
    plt.scatter(y_test, lr_y_pred)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Linear Regression')
    plt.show()
    
    plt.scatter(y_test, rf_y_pred)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Random Forest Regressor')
    plt.show()
    
    plt.scatter(y_test, gb_y_pred)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Gradient Boosting Regressor')
    plt.show()
    
    plt.scatter(y_test, en_y_pred)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Elastic Net Regressor')
    plt.show()


# Main function
def main():
    # Load configuration settings
    file_path = config.FILE_PATH
    target_variable = config.TARGET_VARIABLE
    
    # Load and prepare data
    X_train, X_test, y_train, y_test = load_data(file_path, target_variable)
    
    # Create a data preprocessing pipeline
    numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X_train.select_dtypes(include=['object']).columns
    pipeline = create_pipeline(numeric_features, categorical_features)
    
    # Create and train models
    lr_model, rf_model, gb_model, en_model = train_models(X_train, y_train, pipeline)
    
    # Perform hyperparameter tuning
    grid_search_lr, grid_search_rf, grid_search_gb, grid_search_en = tune_hyperparameters(lr_model, rf_model, gb_model, en_model, X_train, y_train)
    
    # Evaluate models
    evaluate_models(grid_search_lr, grid_search_rf, grid_search_gb, grid_search_en, X_test, y_test)
    
    # Visualize results
    visualize_results(grid_search_lr, grid_search_rf, grid_search_gb, grid_search_en, X_test, y_test)

if __name__ == "__main__":
    main()
