# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.inspection import permutation_importance
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve


# Load and prepare data
def load_data(file_path):
    """Load dataset from CSV file and split into training and testing sets."""
    df = pd.read_csv(file_path)
    X = df.drop('target_variable', axis=1)
    y = df['target_variable']
    X.fillna(X.mean(), inplace=True)
    y.fillna(y.mean(), inplace=True)
    return train_test_split(X, y, test_size=0.2, random_state=42)


# Data preprocessing pipeline
def create_pipeline():
    """Create a data preprocessing pipeline with feature scaling and selection."""
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('selector', SelectKBest(f_regression, k=5))
    ])
    return pipeline


# Create and train models
def train_models(X_train, y_train):
    """Create and train linear regression, random forest, and gradient boosting models."""
    lr_model = Pipeline([
        ('preprocessing', create_pipeline()),
        ('lr', LinearRegression())
    ])
    rf_model = Pipeline([
        ('preprocessing', create_pipeline()),
        ('rf', RandomForestRegressor(n_estimators=100))
    ])
    gb_model = Pipeline([
        ('preprocessing', create_pipeline()),
        ('gb', GradientBoostingRegressor(n_estimators=100))
    ])
    lr_model.fit(X_train, y_train)
    rf_model.fit(X_train, y_train)
    gb_model.fit(X_train, y_train)
    return lr_model, rf_model, gb_model


# Hyperparameter tuning
def tune_hyperparameters(lr_model, rf_model, gb_model, X_train, y_train):
    """Perform hyperparameter tuning using GridSearchCV."""
    param_grid_lr = {'lr__C': [0.1, 1, 10]}
    param_grid_rf = {'rf__n_estimators': [50, 100, 200], 'rf__max_depth': [5, 10, 15]}
    param_grid_gb = {'gb__n_estimators': [50, 100, 200], 'gb__learning_rate': [0.1, 0.5, 1]}
    grid_search_lr = GridSearchCV(lr_model, param_grid_lr, cv=5)
    grid_search_rf = GridSearchCV(rf_model, param_grid_rf, cv=5)
    grid_search_gb = GridSearchCV(gb_model, param_grid_gb, cv=5)
    grid_search_lr.fit(X_train, y_train)
    grid_search_rf.fit(X_train, y_train)
    grid_search_gb.fit(X_train, y_train)
    return grid_search_lr, grid_search_rf, grid_search_gb


# Evaluate models
def evaluate_models(grid_search_lr, grid_search_rf, grid_search_gb, X_test, y_test):
    """Evaluate model performance using mean squared error and R2 score."""
    lr_y_pred = grid_search_lr.predict(X_test)
    rf_y_pred = grid_search_rf.predict(X_test)
    gb_y_pred = grid_search_gb.predict(X_test)
    lr_mse = mean_squared_error(y_test, lr_y_pred)
    lr_r2 = r2_score(y_test, lr_y_pred)
    rf_mse = mean_squared_error(y_test, rf_y_pred)
    rf_r2 = r2_score(y_test, rf_y_pred)
    gb_mse = mean_squared_error(y_test, gb_y_pred)
    gb_r2 = r2_score(y_test, gb_y_pred)
    print("Linear Regression:")
    print(f"MSE: {lr_mse:.2f}, R2: {lr_r2:.2f}")
    print("Random Forest Regressor:")
    print(f"MSE: {rf_mse:.2f}, R2: {rf_r2:.2f}")
    print("Gradient Boosting Regressor:")
    print(f"MSE: {gb_mse:.2f}, R2: {gb_r2:.2f}")


# Visualize results
def visualize_results(grid_search_lr, grid_search_rf, grid_search_gb, X_test, y_test):
    """Visualize model performance using scatter plots and feature importance."""
    # Plot predicted vs actual values
    plt.scatter(y_test, grid_search_lr.predict(X_test), label='Linear Regression')
    plt.scatter(y_test, grid_search_rf.predict(X_test), label='Random Forest Regressor')
    plt.scatter(y_test, grid_search_gb.predict(X_test), label='Gradient Boosting Regressor')
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.legend()
    plt.show()

    # Plot feature importances
    feature_importances_lr = grid_search_lr.best_estimator_.named_steps['lr'].coef_
    feature_importances_rf = grid_search_rf.best_estimator_.named_steps['rf'].feature_importances_
    feature_importances_gb = grid_search_gb.best_estimator_.named_steps['gb'].feature_importances_

    plt.barh(X_test.columns, feature_importances_lr)
    plt.xlabel('Feature Importance')
    plt.ylabel('Features')
    plt.title('Linear Regression Feature Importances')
    plt.show()

    plt.barh(X_test.columns, feature_importances_rf)
    plt.xlabel('Feature Importance')
    plt.ylabel('Features')
    plt.title('Random Forest Regressor Feature Importances')
    plt.show()

    plt.barh(X_test.columns, feature_importances_gb)
    plt.xlabel('Feature Importance')
    plt.ylabel('Features')
    plt.title('Gradient Boosting Regressor Feature Importances')
    plt.show()


# Main function
def main():
    file_path = 'your_data.csv'  # replace with your dataset file path
    X_train, X_test, y_train, y_test = load_data(file_path)
    lr_model, rf_model, gb_model = train_models(X_train, y_train)
    grid_search_lr, grid_search_rf, grid_search_gb = tune_hyperparameters(lr_model, rf_model, gb_model, X_train, y_train)
    evaluate_models(grid_search_lr, grid_search_rf, grid_search_gb, X_test, y_test)
    visualize_results(grid_search_lr, grid_search_rf, grid_search_gb, X_test, y_test)


if __name__ == "__main__":
    main()

