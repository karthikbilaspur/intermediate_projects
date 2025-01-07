from flask_sqlalchemy import SQLAlchemy
from config.settings import Settings

db = SQLAlchemy()

def init_app(app):
    app.config.from_object(Settings)
    db.init_app(app)

def create_tables():
    with db.app.app_context():
        db.create_all()