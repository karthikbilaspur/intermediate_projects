# Import necessary libraries
import tweepy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Set up Tweepy API credentials
consumer_key = "your_consumer_key_here"
consumer_secret = "your_consumer_secret_here"
access_token = "your_access_token_here"
access_token_secret = "your_access_token_secret_here"

# Set up Tweepy API object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define a function to fetch tweets
def fetch_tweets(query, count):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en").items(count)
    return tweets

# Define a function to perform sentiment analysis using NLTK
def nltk_sentiment_analysis(tweet):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(tweet)
    return sentiment

# Define a function to perform sentiment analysis using TextBlob
def textblob_sentiment_analysis(tweet):
    analysis = TextBlob(tweet)
    return analysis.sentiment

# Define a function to perform sentiment analysis using scikit-learn
def sklearn_sentiment_analysis(tweets):
    # Create a list of tweets and their corresponding sentiments
    data = []
    for tweet in tweets:
        sentiment = nltk_sentiment_analysis(tweet.text)
        if sentiment['compound'] >= 0.05:
            sentiment = "Positive"
        elif sentiment['compound'] <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        data.append([tweet.text, sentiment])

    # Split the data into training and testing sets
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the training data and transform both the training and testing data
    X_train = vectorizer.fit_transform([tweet[0] for tweet in train_data])
    y_train = [tweet[1] for tweet in train_data]
    X_test = vectorizer.transform([tweet[0] for tweet in test_data])
    y_test = [tweet[1] for tweet in test_data]

    # Train a Multinomial Naive Bayes classifier
    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    # Make predictions on the testing data
    y_pred = clf.predict(X_test)

    # Evaluate the classifier
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

# Fetch tweets
tweets = fetch_tweets("python", 100)

# Perform sentiment analysis using NLTK
for tweet in tweets:
    sentiment = nltk_sentiment_analysis(tweet.text)
    print("Tweet:", tweet.text)
    print("Sentiment:", sentiment)
    print()

# Perform sentiment analysis using TextBlob
for tweet in tweets:
    sentiment = textblob_sentiment_analysis(tweet.text)
    print("Tweet:", tweet.text)
    print("Sentiment:", sentiment)
    print()

# Perform sentiment analysis using scikit-learn
def sklearn_sentiment_analysis(tweets):
    # Create a list of tweets and their corresponding sentiments
    data = []
    for tweet in tweets:
        sentiment = nltk_sentiment_analysis(tweet.text)
        if sentiment['compound'] >= 0.05:
            sentiment = "Positive"
        elif sentiment['compound'] <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        data.append([tweet.text, sentiment])

    # Split the data into training and testing sets
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the training data and transform both the training and testing data
    X_train = vectorizer.fit_transform([tweet[0] for tweet in train_data])
    y_train = [tweet[1] for tweet in train_data]
    X_test = vectorizer.transform([tweet[0] for tweet in test_data])
    y_test = [tweet[1] for tweet in test_data]

    # Train a Multinomial Naive Bayes classifier
    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    # Make predictions on the testing data
    y_pred = clf.predict(X_test)

    # Evaluate the classifier
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

# Fetch tweets
tweets = fetch_tweets("python", 100)

# Perform sentiment analysis using scikit-learn
sklearn_sentiment_analysis(tweets)