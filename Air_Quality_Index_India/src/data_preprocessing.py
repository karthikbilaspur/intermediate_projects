import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_data(file_path):
    """Load the dataset from a CSV file."""
    return pd.read_csv(file_path)

def handle_missing_values(df):
    """Handle missing values in the dataset."""
    df.fillna(df.mean(), inplace=True)
    return df

def encode_categorical_variables(df):
    """Encode categorical variables using LabelEncoder."""
    le = LabelEncoder()
    df['state'] = le.fit_transform(df['state'])
    df['location'] = le.fit_transform(df['location'])
    df['agency'] = le.fit_transform(df['agency'])
    df['type'] = le.fit_transform(df['type'])
    return df

def save_preprocessed_data(df, file_path):
    """Save the preprocessed data to a CSV file."""
    df.to_csv(file_path, index=False)