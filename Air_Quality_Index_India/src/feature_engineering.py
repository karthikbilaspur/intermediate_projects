import pandas as pd
from sklearn.preprocessing import StandardScaler

def scale_data(df):
    """Scale the data using StandardScaler."""
    scaler = StandardScaler()
    df[['so2', 'no2', 'rspm', 'spm', 'pm2_5']] = scaler.fit_transform(df[['so2', 'no2', 'rspm', 'spm', 'pm2_5']])
    return df