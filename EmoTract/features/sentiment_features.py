from sklearn.feature_extraction.text import TfidfVectorizer

class SentimentFeatures:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def transform(self, text):
        return self.vectorizer.transform(text)