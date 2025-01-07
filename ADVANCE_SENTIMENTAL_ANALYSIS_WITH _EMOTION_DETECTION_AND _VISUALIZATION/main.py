import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from textblob import TextBlob
import seaborn as sns
import pandas as pd

class SentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text):
        scores = self.sia.polarity_scores(text)
        compound_score = scores['compound']

        if compound_score >= 0.05:
            return "Positive", scores
        elif compound_score <= -0.05:
            return "Negative", scores
        else:
            return "Neutral", scores

    def detect_emotions(self, text):
        blob = TextBlob(text)
        emotions = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
        return emotions

    def visualize_sentiment(self, texts, sentiments, emotions):
        sentiment_counts = pd.Series(sentiments).value_counts()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
        plt.title("Sentiment Distribution")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        plt.show()

        emotion_df = pd.DataFrame(emotions)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=emotion_df['polarity'], y=emotion_df['subjectivity'])
        plt.title("Emotion Intensity")
        plt.xlabel("Polarity")
        plt.ylabel("Subjectivity")
        plt.show()


# Example usage
analyzer = SentimentAnalyzer()
texts = [
    "I love this product! It's amazing.",
    "I'm disappointed with this product.",
    "This product is okay.",
    "Excellent customer service!",
    "Terrible experience."
]

sentiments = []
emotions = []
for text in texts:
    sentiment, scores = analyzer.analyze_sentiment(text)
    emotion = analyzer.detect_emotions(text)
    print(f"Text: {text}\nSentiment: {sentiment}\nScores: {scores}\nEmotions: {emotion}\n")
    sentiments.append(sentiment)
    emotions.append(emotion)

analyzer.visualize_sentiment(texts, sentiments, emotions)