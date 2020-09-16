class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://pgadmin:pgadmin@db:5432/news_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test'
    DEBUG = False
    CSRF_ENABLED = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'pocketnewsnetwork@gmail.com'
    MAIL_PASSWORD = 'PocketNews123'
