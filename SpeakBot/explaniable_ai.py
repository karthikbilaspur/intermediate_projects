import lime
from lime.lime_text import LimeTextExplainer

class ExplainableAI:
    def __init__(self):
        self.explainer = LimeTextExplainer()

    def explain_prediction(self, text, prediction):
        explanation = self.explainer.explain_instance(text, prediction)
        return explanation.as_list()