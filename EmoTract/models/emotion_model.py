from sklearn.ensemble import RandomForestClassifier

class EmotionModel:
    def __init__(self):
        self.model = RandomForestClassifier()

    def predict(self, text, features):
        vectorized_text = features.transform([text])
        return self.model.predict(vectorized_text)