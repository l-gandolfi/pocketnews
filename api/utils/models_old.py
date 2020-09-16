from api import db
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa

# N:N 
interested_in = db.Table('interested_in', 
                db.Column('consumer_id', db.Integer, db.ForeignKey('consumer.id', ondelete='CASCADE')),
                db.Column('topic_id', db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'))
)

# N:N Relationship with attributes
class Like(db.Model):
    __tablename__ = 'liked'
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id', ondelete="CASCADE"), primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete="CASCADE"), primary_key=True)
    initial = db.Column(db.Boolean, nullable=False)
    utente = db.relationship("Consumer", back_populates="news_like")
    news = db.relationship("News", back_populates="utente_like")

# N:N Relationship with attributes
class Recommended(db.Model):
    __tablename__ = 'recommended_to'
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id', ondelete="CASCADE"), primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete="CASCADE"), primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    utente = db.relationship("Consumer", back_populates="news_recommended")
    news = db.relationship("News", back_populates="recommended_consumer")

class Consumer(db.Model):
    __tablename__ = 'consumer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    surname = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email_checked = db.Column(db.Boolean(), nullable=False)
    reset_psw_date = db.Column(db.DateTime, nullable=True)
    reset_done = db.Column(db.Boolean(), nullable=False)
    city = db.Column(db.String(30), nullable=True)
    bio = db.Column(db.String(150), nullable=True)
    dob = db.Column(db.String(30), nullable=True)
    publicinfo = db.Column(db.String(5), nullable=True)
    interested = db.relationship("Topic", secondary=interested_in, backref=db.backref('subscribe', lazy='dynamic'), cascade="all, delete", passive_deletes=True)
    news_like = db.relationship("Like", back_populates="utente", cascade="all, delete", passive_deletes=True)
    news_recommended = db.relationship("Recommended", back_populates="utente", cascade="all, delete", passive_deletes=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "username": self.username,
        }

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2572), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    embedding = db.Column(postgresql.ARRAY(sa.Float, dimensions=1), unique=False, nullable=False)
    author = db.Column(db.String(40), unique=False, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False)
    utente_like = db.relationship("Like", back_populates="news", cascade="all, delete", passive_deletes=True)
    recommended_consumer = db.relationship("Recommended", back_populates="news", cascade="all, delete", passive_deletes=True)

    def to_json(self):
        return {
            "id": self.id,
            "text": self.text,
            "date": self.date.strftime("%d/%m/%Y"),
            "author": self.author,
        }

class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20), unique=False, nullable=False)
    news = db.relationship('News', backref='news', lazy=True, cascade="all, delete", passive_deletes=True)

class Session(db.Model):
	__tablename__ = 'session'
	user_id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.String(10), primary_key=True, nullable=False)
