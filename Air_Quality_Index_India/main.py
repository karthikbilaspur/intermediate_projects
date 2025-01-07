# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('data.csv')

# Preprocess the data
df['sampling_date'] = pd.to_datetime(df['sampling_date'])
df['state'] = LabelEncoder().fit_transform(df['state'])
df['location'] = LabelEncoder().fit_transform(df['location'])
df['agency'] = LabelEncoder().fit_transform(df['agency'])
df['type'] = LabelEncoder().fit_transform(df['type'])

# Handle missing values
df.fillna(df.mean(), inplace=True)

# Define features and target
X = df.drop(['AQI'], axis=1)
y = df['AQI']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Apply PCA to reduce dimensionality
pca = PCA(n_components=0.95)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

# Select K-best features using f-regression
selector = SelectKBest(f_regression, k=10)
X_train_selected = selector.fit_transform(X_train_pca, y_train)
X_test_selected = selector.transform(X_test_pca)

# Train a Random Forest Regressor
rf_model = RandomForestRegressor()
rf_model.fit(X_train_selected, y_train)
y_pred_rf = rf_model.predict(X_test_selected)
print(f'Random Forest Regressor MSE: {mean_squared_error(y_test, y_pred_rf)}')

# Train an Ada Boost Regressor
ada_model = AdaBoostRegressor()
ada_model.fit(X_train_selected, y_train)
y_pred_ada = ada_model.predict(X_test_selected)
print(f'Ada Boost Regressor MSE: {mean_squared_error(y_test, y_pred_ada)}')

# Train a Bagging Regressor
bag_model = BaggingRegressor()
bag_model.fit(X_train_selected, y_train)
y_pred_bag = bag_model.predict(X_test_selected)
print(f'Bagging Regressor MSE: {mean_squared_error(y_test, y_pred_bag)}')

# Train a Linear Regression model
lr_model = LinearRegression()
lr_model.fit(X_train_selected, y_train)
y_pred_lr = lr_model.predict(X_test_selected)
print(f'Linear Regression MSE: {mean_squared_error(y_test, y_pred_lr)}')

# Plot the results
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred_rf, label='Random Forest Regressor')
sns.scatterplot(x=y_test, y=y_pred_ada, label='Ada Boost Regressor')
sns.scatterplot(x=y_test, y=y_pred_bag, label='Bagging Regressor')
sns.scatterplot(x=y_test, y=y_pred_lr, label='Linear Regression')
plt.xlabel('Actual AQI')
plt.ylabel('Predicted AQI')
plt.title('Air Quality Index Prediction')
plt.legend()
plt.show()