from api import db, ma

from .interested_in import Interested_in
from .follows import Consumer_following


class Consumer(db.Model):
    __tablename__ = 'consumer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    surname = db.Column(db.String(20), unique=False)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60))
    email_checked = db.Column(db.Boolean())
    email_token = db.Column(db.String(10))
    reset_psw_date = db.Column(db.DateTime)
    reset_done = db.Column(db.Boolean())
    city = db.Column(db.String(30))
    bio = db.Column(db.String(150))
    dob = db.Column(db.String(30))
    publicinfo = db.Column(db.String(5))
    interested = db.relationship("Topic", secondary=Interested_in, backref=db.backref('subscribe', lazy='dynamic'), cascade="all, delete", passive_deletes=True)
    news_like = db.relationship("Like", back_populates="utente", cascade="all, delete", passive_deletes=True)
    news_recommended = db.relationship("Recommended", back_populates="utente", cascade="all, delete", passive_deletes=True)
    followers = db.relationship(
        'Consumer', lambda: Consumer_following,
        primaryjoin=lambda: Consumer.id == Consumer_following.c.consumer_id,
        secondaryjoin=lambda: Consumer.id == Consumer_following.c.following_id,
        backref='following'
    )
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "username": self.username,
        }

class ConsumerSchema(ma.SQLAlchemySchema):
    class Meta:
        # Full exposure
        model = Consumer
        # Otherwise
        #fields = ("email", "date_created", "_links")
