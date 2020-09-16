from api import db

# N:N Relationship with attributes
class Recommended(db.Model):
    __tablename__ = 'recommended_to'
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id', ondelete="CASCADE"), primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete="CASCADE"), primary_key=True)
    date = db.Column(db.DateTime)
    score = db.Column(db.Integer)
    utente = db.relationship("Consumer", back_populates="news_recommended")
    news = db.relationship("News", back_populates="recommended_consumer")