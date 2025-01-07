import spacy

class NLP:
    def __init__(self):
        self.model = spacy.load("en_core_web_sm")

    def process_text(self, text):
        return self.model(text)