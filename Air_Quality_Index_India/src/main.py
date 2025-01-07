import pandas as pd
from sklearn.model_selection import train_test_split
from src.data_preprocessing import load_data, handle_missing_values, encode_categorical_variables
from src.feature_engineering import scale_data
from src.model_training import train_random_forest_regressor, train_ada_boost_regressor, train_bagging_regressor, train_linear_regression
from src.model_evaluation import load_models, evaluate_models

def main():
    # Load the dataset
    df = load_data('data.csv')

    # Preprocess the data
    df = handle_missing_values(df)
    df = encode_categorical_variables(df)

    # Split the data into training and testing sets
    X = df.drop(['AQI'], axis=1)
    y = df['AQI']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale the data
    X_train = scale_data(X_train)
    X_test = scale_data(X_test)

    # Train the models
    rf_model = train_random_forest_regressor(X_train, y_train)
    ada_model = train_ada_boost_regressor(X_train, y_train)
    bag_model = train_bagging_regressor(X_train, y_train)
    lr_model = train_linear_regression(X_train, y_train)

    # Save the trained models
    import pickle
    with open('rf_model.pkl', 'wb') as f:
        pickle.dump(rf_model, f)
    with open('ada_model.pkl', 'wb') as f:
        pickle.dump(ada_model, f)
    with open('bag_model.pkl', 'wb') as f:
        pickle.dump(bag_model, f)
    with open('lr_model.pkl', 'wb') as f:
        pickle.dump(lr_model, f)

    # Evaluate the models
    rf_model, ada_model, bag_model, lr_model = load_models()
    evaluate_models(rf_model, ada_model, bag_model, lr_model, X_test, y_test)

if __name__ == '__main__':
    main()