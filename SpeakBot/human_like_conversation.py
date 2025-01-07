import nltk
from nltk.probability import ProbabilityDistribution

class HumanLikeConversations:
    def __init__(self):
        self.response_distribution = ProbabilityDistribution()

    def generate_response(self, intent, entities):
        responses = self.response_distribution[intent]
        return responses.sample()