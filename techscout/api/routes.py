from flask import request
from utils.db import create_article, update_article, delete_article

@api.route('/articles/<int:id>')
class Article(Resource):
    def get(self, id):
        article = get_article(id)
        return jsonify(article)

    def put(self, id):
        data = request.get_json()
        update_article(id, data)
        return jsonify({'message': 'Article updated'})

    def delete(self, id):
        delete_article(id)
        return jsonify({'message': 'Article deleted'})

@api.route('/articles')
class CreateArticle(Resource):
    def post(self):
        data = request.get_json()
        create_article(data)
        return jsonify({'message': 'Article created'})