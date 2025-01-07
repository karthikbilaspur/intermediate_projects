class Settings:
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///emotract.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = False
    FLASK_ENV = 'development'
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'