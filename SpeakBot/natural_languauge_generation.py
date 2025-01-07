import nltk
from nltk.tokenize import word_tokenize

class NaturalLanguageGenerator:
    def __init__(self):
        self.templates = {
            "greeting": "Hello, {name}!",
            "farewell": "Goodbye, {name}!"
        }

    def generate_text(self, template, variables):
        text = self.templates[template]
        for var, value in variables.items():
            text = text.replace(f"{{{var}}}", value)
        return text