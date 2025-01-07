from sklearn.feature_extraction.text import TfidfVectorizer

class AspectFeatures:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def transform(self, text):
        return self.vectorizer.transform(text)