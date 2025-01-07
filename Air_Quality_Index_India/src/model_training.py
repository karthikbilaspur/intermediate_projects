import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LinearRegression
import pickle

def train_random_forest_regressor(X_train, y_train):
    """Train a Random Forest Regressor."""
    rf_model = RandomForestRegressor()
    rf_model.fit(X_train, y_train)
    return rf_model

def train_ada_boost_regressor(X_train, y_train):
    """Train an Ada Boost Regressor."""
    ada_model = AdaBoostRegressor()
    ada_model.fit(X_train, y_train)
    return ada_model

def train_bagging_regressor(X_train, y_train):
    """Train a Bagging Regressor."""
    bag_model = BaggingRegressor()
    bag_model.fit(X_train, y_train)
    return bag_model

def train_linear_regression(X_train, y_train):
    """Train a Linear Regression model."""
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    return lr_model

def save_models(rf_model, ada_model, bag_model, lr_model):
    """Save the trained models to pickle files."""
    with open('rf_model.pkl', 'wb') as f:
        pickle.dump(rf_model, f)
    with open('ada_model.pkl', 'wb') as f:
        pickle.dump(ada_model, f)
    with open('bag_model.pkl', 'wb') as f:
        pickle.dump(bag_model, f)
    with open('lr_model.pkl', 'wb') as f:
        pickle.dump(lr_model, f)