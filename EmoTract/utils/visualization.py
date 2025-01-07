import matplotlib.pyplot as plt

class Visualization:
    def __init__(self):
        pass

    def visualize_sentiment(self, sentiment):
        plt.bar(sentiment.keys(), sentiment.values())
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.title('Sentiment Distribution')
        plt.show()