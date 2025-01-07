from flask import Flask, render_template, request, redirect, url_for
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from gensim.summarization import summarize
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from textstat.textstat import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from bs4 import BeautifulSoup
import requests

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

app = Flask(__name__)

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [word for word in words if word not in stop_words]
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return words

def summarize_text(text, method='sentence_scoring'):
    if method == 'sentence_scoring':
        sentence_scores = {}
        sentences = sent_tokenize(text)
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in preprocess_text(text):
                    if sentence in sentence_scores:
                        sentence_scores[sentence] += 1
                    else:
                        sentence_scores[sentence] = 1
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        summary = ' '.join([sentence for sentence, score in top_sentences])
    elif method == 'gensim':
        summary = summarize(text, ratio=0.5)
    elif method == 'tfidf':
        dictionary = Dictionary([preprocess_text(text)])
        corpus = [dictionary.doc2bow(preprocess_text(text))]
        tfidf = TfidfModel(corpus)
        sentences = sent_tokenize(text)
        sentence_scores = {}
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            words = [word for word in words if word not in stopwords.words('english')]
            sentence_corpus = dictionary.doc2bow(words)
            sentence_tfidf = tfidf[sentence_corpus]
            score = sum([tfidf_score for word, tfidf_score in sentence_tfidf])
            sentence_scores[sentence] = score
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        summary = ' '.join([sentence for sentence, score in top_sentences])
    elif method == 'cosine_similarity':
        sentences = sent_tokenize(text)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sentences)
        similarity_matrix = cosine_similarity(tfidf_matrix)
        sentence_scores = {}
        for i in range(len(sentences)):
            score = 0
            for j in range(len(sentences)):
                if i != j:
                    score += similarity_matrix[i][j]
            sentence_scores[sentences[i]] = score
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        summary = ' '.join([sentence for sentence, score in top_sentences])
    return summary

def fetch_news(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text
    except Exception as e:
        return str(e)

def sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    return sentiment_scores

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        method = request.form['method']
        text = fetch_news(url)
        if text:
            summary = summarize_text(text, method)
            sentiment = sentiment_analysis(summary)
            return render_template('summary.html', summary=summary, sentiment=sentiment)
        else:
            return render_template('error.html')
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)