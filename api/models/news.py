from api import db
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2572), unique=False)
    date = db.Column(db.DateTime, unique=False)
    embedding = db.Column(postgresql.ARRAY(sa.Float, dimensions=1), unique=False)
    author = db.Column(db.String(40), unique=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'))
    utente_like = db.relationship("Like", back_populates="news", cascade="all, delete", passive_deletes=True)
    recommended_consumer = db.relationship("Recommended", back_populates="news", cascade="all, delete", passive_deletes=True)

    def to_json(self):
        return {
            "id": self.id,
            "text": self.text,
            "date": self.date.strftime("%d/%m/%Y"),
            "author": self.author,
            "topic_id": self.topic_id
        }