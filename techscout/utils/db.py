import sqlite3

def get_articles():
    conn = sqlite3.connect('techcrunch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()
    return articles

def get_article(id):
    conn = sqlite3.connect('techcrunch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles WHERE id=?', (id,))
    article = cursor.fetchone()
    return article

def create_article(data):
    conn = sqlite3.connect('techcrunch.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO articles (title, link, description)
        VALUES (?, ?, ?)
    ''', (data['title'], data['link'], data['description']))
    conn.commit()

def update_article(id, data):
    conn = sqlite3.connect('techcrunch.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE articles
        SET title=?, link=?, description=?
        WHERE id=?
    ''', (data['title'], data['link'], data['description'], id))
    conn.commit()

def delete_article(id):
    conn = sqlite3.connect('techcrunch.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM articles WHERE id=?', (id,))
    conn.commit()