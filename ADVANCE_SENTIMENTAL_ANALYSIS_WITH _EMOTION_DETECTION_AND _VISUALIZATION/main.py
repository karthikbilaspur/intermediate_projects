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
        """
        Analyze sentiment of a given text.

        Args:
            text (str): Text to analyze.

        Returns:
            tuple: Sentiment classification ("Positive", "Negative", or "Neutral") and sentiment scores.
        """
        scores = self.sia.polarity_scores(text)
        compound_score = scores['compound']

        if compound_score >= 0.05:
            return "Positive", scores
        elif compound_score <= -0.05:
            return "Negative", scores
        else:
            return "Neutral", scores

    def detect_emotions(self, text):
        """
        Detect emotions in a given text.

        Args:
            text (str): Text to analyze.

        Returns:
            dict: Dictionary containing polarity and subjectivity scores.
        """
        blob = TextBlob(text)
        emotions = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
        return emotions

    def visualize_sentiment(self, texts, sentiments, emotions):
        """
        Visualize sentiment distribution and emotion intensity.

        Args:
            texts (list): List of texts.
            sentiments (list): List of sentiment classifications.
            emotions (list): List of emotion dictionaries.
        """
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

    def analyze_and_visualize(self, texts):
        """
        Analyze sentiment and detect emotions for a list of texts, then visualize the results.

        Args:
            texts (list): List of texts to analyze.

        Returns:
            tuple: List of sentiment classifications and list of emotion dictionaries.
        """
        sentiments = []
        emotions = []
        for text in texts:
            sentiment, scores = self.analyze_sentiment(text)
            emotion = self.detect_emotions(text)
            print(f"Text: {text}\nSentiment: {sentiment}\nScores: {scores}\nEmotions: {emotion}\n")
            sentiments.append(sentiment)
            emotions.append(emotion)

        self.visualize_sentiment(texts, sentiments, emotions)
        return sentiments, emotions

    def save_results(self, texts, sentiments, emotions, filename):
        """
        Save sentiment analysis and emotion detection results to a CSV file.

        Args:
            texts (list): List of texts.
            sentiments (list): List of sentiment classifications.
            emotions (list): List of emotion dictionaries.
            filename (str): Name of the CSV file.
        """
        results = pd.DataFrame({
            'Text': texts,
            'Sentiment': sentiments,
            'Polarity': [emotion['polarity'] for emotion in emotions],
            'Subjectivity': [emotion['subjectivity'] for emotion in emotions]
        })
        results.to_csv(filename, index=False)


# Enhanced functionality
# - Added return values to analyze_and_visualize method
# - Introduced save_results method to save analysis results to a CSV file