from flask import Flask, jsonify
from flask_restx import Api, Resource
from utils.db import get_articles

app = Flask(__name__)
api = Api(app)

@api.route('/articles')
class Articles(Resource):
    def get(self):
        articles = get_articles()
        return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)