from api import db

class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20), unique=False)
    news = db.relationship('News', backref='news', lazy=True, cascade="all, delete", passive_deletes=True)
