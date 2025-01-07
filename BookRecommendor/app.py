from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import json
from datetime import datetime
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
app.secret_key = 'book_recommendation'

# Load book and user data
with open('data.json') as f:
    books = json.load(f)

with open('users.json') as f:
    users = json.load(f)

# User profiling
def update_user_profile(user_id, book_id, rating):
    users[user_id]['reading_history'].append({'book_id': book_id, 'rating': rating})
    users[user_id]['preferences'] = calculate_preferences(users[user_id]['reading_history'])

def calculate_preferences(reading_history):
    preferences = defaultdict(int)
    for book in reading_history:
        book_attributes = books[str(book['book_id'])]
        preferences['author'] += book_attributes['author']
        preferences['publisher'] += book_attributes['publisher']
        preferences['genre'] += book_attributes['genre']
    return dict(preferences)

# Collaborative filtering
def collaborative_filtering(user_id):
    similarities = []
    for other_user in users:
        if other_user != user_id:
            similarity = cosine_similarity([users[user_id]['preferences']], [users[other_user]['preferences']])[0][0]
            similarities.append((other_user, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    recommendations = []
    for similar_user, _ in similarities[:5]:
        for book in users[similar_user]['reading_history']:
            if book['book_id'] not in [b['book_id'] for b in users[user_id]['reading_history']]:
                recommendations.append(books[str(book['book_id'])])
    return recommendations

# Content-based filtering
def content_based_filtering(user_id):
    user_preferences = users[user_id]['preferences']
    recommendations = []
    for book in books.values():
        book_attributes = {'author': book['author'], 'publisher': book['publisher'], 'genre': book['genre']}
        similarity = cosine_similarity([user_preferences], [book_attributes])[0][0]
        if similarity > 0.5 and book['id'] not in [b['book_id'] for b in users[user_id]['reading_history']]:
            recommendations.append(book)
    return recommendations

# Real-time processing
def real_time_recommendations(user_id):
    return collaborative_filtering(user_id) + content_based_filtering(user_id)

# Evaluation metrics
def precision(recommendations, user_id):
    relevant_books = [book for book in users[user_id]['reading_history'] if book['rating'] > 3]
    return len(set(recommendations) & set(relevant_books)) / len(recommendations)

def recall(recommendations, user_id):
    relevant_books = [book for book in users[user_id]['reading_history'] if book['rating'] > 3]
    return len(set(recommendations) & set(relevant_books)) / len(relevant_books)

@app.route('/')
def index():
    return render_template('index.html', books=list(books.values()))

@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = session['user_id']
    recommendations = real_time_recommendations(user_id)
    return render_template('recommend.html', recommendations=recommendations)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        user_id = session['user_id']
        book_id = request.form['book_id']
        rating = int(request.form['rating'])
        update_user_profile(user_id, book_id, rating)
    return render_template('profile.html', user=users[session['user_id']])

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    for user in users:
        if users[user]['username'] == username:
            session['user_id'] = user
            return redirect(url_for('index'))
    return 'Invalid username', 401

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/login_page')
def login_page():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)