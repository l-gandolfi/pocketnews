from api import db

# N:N Relationship with attributes
class Like(db.Model):
    __tablename__ = 'liked'
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id', ondelete="CASCADE"), primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete="CASCADE"), primary_key=True)
    initial = db.Column(db.Boolean)
    utente = db.relationship("Consumer", back_populates="news_like")
    news = db.relationship("News", back_populates="utente_like")
