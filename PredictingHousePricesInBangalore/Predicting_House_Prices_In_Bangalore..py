# Import libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor, StackingRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.neural_network import MLPRegressor
from sklearn.inspection import permutation_importance, partial_dependence
from sklearn.inspection import plot_partial_dependence
import matplotlib.pyplot as plt
import seaborn as sns
import shap

# Load dataset
df = pd.read_csv('bangalore_house_prices.csv')

# Preprocess data
df = df.dropna()
df = df.drop_duplicates()

# Define features (X) and target variable (y)
X = df[['Area', 'Bedrooms', 'Bathrooms', 'Floor', 'Age', 'Locality', 'Neighborhood', 'Property_Type']]
y = df['Price']

# Scale numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Polynomial and interaction terms
poly_features = PolynomialFeatures(degree=2)
X_train_poly = poly_features.fit_transform(X_train)
interaction_terms = PolynomialFeatures(interaction_only=True)
X_train_interaction = interaction_terms.fit_transform(X_train)

# PCA for dimensionality reduction
from sklearn.decomposition import PCA
pca = PCA(n_components=0.95)
X_train_pca = pca.fit_transform(X_train)

# Hyperparameter tuning
param_grid_rf = {'n_estimators': [50, 100, 200]}
param_grid_gb = {'n_estimators': [50, 100, 200], 'learning_rate': [0.1, 0.01]}
param_grid_mlp = {'hidden_layer_sizes': [(50, 50), (100, 100)]}
grid_rf = GridSearchCV(RandomForestRegressor(), param_grid_rf, cv=5)
grid_gb = GridSearchCV(GradientBoostingRegressor(), param_grid_gb, cv=5)
grid_mlp = GridSearchCV(MLPRegressor(max_iter=1000), param_grid_mlp, cv=5)

# Ensemble methods
rf_model = RandomForestRegressor(n_estimators=100)
gb_model = GradientBoostingRegressor(n_estimators=100)
voting_model = VotingRegressor(estimators=[('rf', rf_model), ('gb', gb_model)])
stacking_model = StackingRegressor(estimators=[('rf', rf_model), ('gb', gb_model)], final_estimator=LinearRegression())

# Evaluate models
grid_rf.fit(X_train_pca, y_train)
grid_gb.fit(X_train_pca, y_train)
grid_mlp.fit(X_train_pca, y_train)
rf_y_pred = grid_rf.predict(X_test)
gb_y_pred = grid_gb.predict(X_test)
mlp_y_pred = grid_mlp.predict(X_test)
voting_y_pred = voting_model.fit(X_train_pca, y_train).predict(X_test)
stacking_y_pred = stacking_model.fit(X_train_pca, y_train).predict(X_test)

# Model metrics
print("Random Forest Metrics:")
print('MSE:', mean_squared_error(y_test, rf_y_pred))
print('R2 Score:', r2_score(y_test, rf_y_pred))

print("\nGradient Boosting Metrics:")
print('MSE:', mean_squared_error(y_test, gb_y_pred))
print('R2 Score:', r2_score(y_test, gb_y_pred))

print("\nMLP Metrics:")
print('MSE:', mean_squared_error(y_test, mlp_y_pred))
print('R2 Score:', r2_score(y_test, mlp_y_pred))

print("\nVoting Metrics:")
print('MSE:', mean_squared_error(y_test, voting_y_pred))
print('R2 Score:', r2_score(y_test, voting_y_pred))

print("\nStacking Metrics:")
print('MSE:', mean_squared_error(y_test, stacking_y_pred))
print('R2 Score:', r2_score(y_test, stacking_y_pred))

# SHAP values
explainer = shap.Explainer(grid_rf.best_estimator_)
shap_values = explainer(X_test)
shap.plots.waterfall(shap_values[0])
plt.show()

# Partial dependence plots
plot_partial_dependence(grid_rf.best_estimator_, X_train_pca, ['Area', 'Bedrooms'])
plt.show()