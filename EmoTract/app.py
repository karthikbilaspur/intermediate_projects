from flask import Flask, request, render_template
from config.settings import Settings
from models.sentiment_model import SentimentModel
from models.emotion_model import EmotionModel
from models.aspect_model import AspectModel
from features.sentiment_features import SentimentFeatures
from features.emotion_features import EmotionFeatures
from features.aspect_features import AspectFeatures
from data.dataset import Dataset
from data.data_loader import DataLoader
from utils.preprocessing import Preprocessing
from utils.visualization import Visualization

app = Flask(__name__)
app.config.from_object(Settings)

# Initialize sentiment model and train
sentiment_model = SentimentModel()
data = pd.read_csv('sentiment_data.csv')
sentiment_model.train(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']

        # Sentiment Analysis
        sentiment_features = SentimentFeatures()
        sentiment = sentiment_model.predict(text, sentiment_features)

        # Emotion Analysis
        emotion_model = EmotionModel()
        emotion_features = EmotionFeatures()
        emotion = emotion_model.predict(text, emotion_features)

        # Aspect-Based Analysis
        aspect_model = AspectModel()
        aspect_features = AspectFeatures()
        aspect_sentiment = aspect_model.predict(text, aspect_features)

        return render_template('result.html', 
                               text=text, 
                               sentiment=sentiment, 
                               emotion=emotion, 
                               aspect_sentiment=aspect_sentiment)
    return render_template('index.html')