from api import db

# N:N 
Consumer_following = db.Table(
    'Consumer_following',
    db.Column('consumer_id', db.Integer, db.ForeignKey('consumer.id'), primary_key=True),
    db.Column('following_id', db.Integer, db.ForeignKey('consumer.id'), primary_key=True)
)