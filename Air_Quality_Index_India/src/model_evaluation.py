import pandas as pd
import pickle
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

def load_models():
    """Load the trained models from pickle files."""
    with open('rf_model.pkl', 'rb') as f:
        rf_model = pickle.load(f)
    with open('ada_model.pkl', 'rb') as f:
        ada_model = pickle.load(f)
    with open('bag_model.pkl', 'rb') as f:
        bag_model = pickle.load(f)
    with open('lr_model.pkl', 'rb') as f:
        lr_model = pickle.load(f)
    return rf_model, ada_model, bag_model, lr_model

def evaluate_models(rf_model, ada_model, bag_model, lr_model, X_test, y_test):
    """Evaluate the trained models."""
    rf_y_pred = rf_model.predict(X_test)
    ada_y_pred = ada_model.predict(X_test)
    bag_y_pred = bag_model.predict(X_test)
    lr_y_pred = lr_model.predict(X_test)

    print("Random Forest Regressor:")
    print(f"MSE: {mean_squared_error(y_test, rf_y_pred)}")
    print(f"R2 Score: {r2_score(y_test, rf_y_pred)}")

    print("\nAda Boost Regressor:")
    print(f"MSE: {mean_squared_error(y_test, ada_y_pred)}")
    print(f"R2 Score: {r2_score(y_test, ada_y_pred)}")

    print("\nBagging Regressor:")
    print(f"MSE: {mean_squared_error(y_test, bag_y_pred)}")
    print(f"R2 Score: {r2_score(y_test, bag_y_pred)}")

    print("\nLinear Regression:")
    print(f"MSE: {mean_squared_error(y_test, lr_y_pred)}")
    print(f"R2 Score: {r2_score(y_test, lr_y_pred)}")