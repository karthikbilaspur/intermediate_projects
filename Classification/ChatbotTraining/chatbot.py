# Import necessary libraries
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tensorflow.keras.models import load_model
import spacy
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
import pickle

# Load models and data
def load_models():
    # Load intent recognition model
    intent_model = load_model('intent_recognition_model.h5')
    
    # Load contextual understanding model
    contextual_model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased')
    contextual_tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    
    # Load entity recognizer
    nlp = spacy.load('en_core_web_sm')
    
    # Load sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Load vectorizer
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    
    # Load labels and intents
    labels = np.load('labels.npy')
    intents = np.load('intents.npy', allow_pickle=True).item()
    
    return intent_model, contextual_model, contextual_tokenizer, nlp, sia, vectorizer, labels, intents

# Preprocess user input
def preprocess_input(message):
    # Tokenize message
    tokens = nltk.word_tokenize(message)
    
    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    
    # Join tokens back into a string
    message = ' '.join(tokens)
    
    return message

# Analyze user input
def analyze_input(message, intent_model, contextual_model, contextual_tokenizer, nlp, sia, vectorizer, labels, intents):
    # Vectorize message
    message_vectorized = vectorizer.transform([message])
    
    # Predict intent
    prediction = intent_model.predict(message_vectorized)
    
    # Get label with highest probability
    label = labels[np.argmax(prediction)]
    
    # Analyze sentiment
    sentiment = sia.polarity_scores(message)
    
    # Recognize entities
    entities = nlp(message)
    
    # Understand context
    input_ids = contextual_tokenizer.encode(message, return_tensors='pt')
    attention_mask = contextual_tokenizer.encode(message, return_tensors='pt', max_length=512, padding='max_length', truncation=True)
    outputs = contextual_model(input_ids, attention_mask=attention_mask)
    
    return label, sentiment, entities, outputs

# Generate response
def generate_response(label, sentiment, entities, outputs, intents):
    # Get intent corresponding to predicted label
    intent = intents['intents'][label]
    
    # Get responses for intent
    responses = intent['responses']
    
    # Generate response based on sentiment, entities, and context
    if sentiment['compound'] > 0.5:
        return random.choice(responses) + " I'm glad you're feeling positive!"
    elif sentiment['compound'] < -0.5:
        return random.choice(responses) + " Sorry to hear you're feeling down."
    else:
        if entities.ents:
            entity = entities.ents[0]
            return f"I see you mentioned {entity.text}. How can I assist you with that?"
        elif outputs:
            return f"Regarding your previous message, {random.choice(responses)}"
        else:
            return random.choice(responses)

# Chatbot function
def chatbot(message, intent_model, contextual_model, contextual_tokenizer, nlp, sia, vectorizer, labels, intents):
    # Preprocess user input
    message = preprocess_input(message)
    
    # Analyze user input
    label, sentiment, entities, outputs = analyze_input(message, intent_model, contextual_model, contextual_tokenizer, nlp, sia, vectorizer, labels, intents)
    
    # Generate response
    response = generate_response(label, sentiment, entities, outputs, intents)
    
    return response

# Load models and data
intent_model, contextual_model, contextual_tokenizer, nlp, sia, vectorizer, labels, intents = load_models()

# Test chatbot
while True:
    message = input('User: ')
    response = chatbot(message, intent_model, contextual_model, contextual_tokenizer, nlp, sia, vectorizer, labels, intents)
    print('Chatbot:', response)