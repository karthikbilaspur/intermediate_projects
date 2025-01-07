import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class Preprocessing:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t.isalpha() and t not in self.stop_words]
        return ' '.join(tokens)