# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly.graph_objects as go
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from surprise import Reader, Dataset, SVD
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load datasets
listings = pd.read_csv('listings.csv')
reviews = pd.read_csv('reviews.csv')
host_profiles = pd.read_csv('host_profiles.csv')

# Data Preparation
listings = listings.dropna()  # Remove missing values
reviews = reviews.dropna()
host_profiles = host_profiles.dropna()

# Geospatial Analysis
m = folium.Map(location=[40.7128, -74.006], zoom_start=12)
for index, row in listings.iterrows():
    folium.CircleMarker([row['latitude'], row['longitude']], radius=3).add_to(m)
m.save('nyc_airbnb_map.html')

# Price Dynamics
prices = listings['price']
plt.figure(figsize=(12, 6))
sns.lineplot(data=prices)
plt.title('Price Fluctuations')
plt.show()

# Room Type Insights
room_types = listings['room_type']
occupancy_rates = listings['occupancy_rate']
prices = listings['price']
sns.catplot(x=room_types, y=occupancy_rates)
sns.catplot(x=room_types, y=prices)
plt.show()

# Host Performance
host_ratings = listings['host_response_rate']
host_listings = listings['host_listings_count']
plt.bar(host_ratings, host_listings)
plt.title('Host Performance')
plt.show()

# Sentiment Analysis
sia = SentimentIntensityAnalyzer()
sentiments = reviews['comments'].apply(sia.polarity_scores)
plt.figure(figsize=(10, 8))
sns.heatmap(sentiments, annot=True, cmap='coolwarm', square=True)
plt.title('Sentiment Analysis')
plt.show()

# Recommendation System
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(listings[['id', 'host_id', 'rating']], reader)
trainset = data.build_full_trainset()
algo = SVD()
algo.fit(trainset)
predictions = algo.test(trainset.build_testset())

# Predictive Modeling
X = listings[['price', 'occupancy_rate', 'room_type']]
y = listings['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Evaluate Predictive Model
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Display Predictions
plt.scatter(y_test, predictions)
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.title('Predictive Modeling')
plt.show()