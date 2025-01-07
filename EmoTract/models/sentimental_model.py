# sentiment_model.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

class SentimentModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, data):
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(data['text'], data['sentiment'], test_size=0.2, random_state=42)

        # Vectorize text data
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        X_test_vectorized = self.vectorizer.transform(X_test)

        # Train model
        self.model.fit(X_train_vectorized, y_train)

        # Evaluate model
        y_pred = self.model.predict(X_test_vectorized)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    def predict(self, text):
        # Vectorize input text
        vectorized_text = self.vectorizer.transform([text])

        # Predict sentiment
        sentiment = self.model.predict(vectorized_text)
        return sentiment[0]

# Load dataset
data = pd.read_csv('sentiment_data.csv')

# Initialize sentiment model
sentiment_model = SentimentModel()

# Train sentiment model
sentiment_model.train(data)