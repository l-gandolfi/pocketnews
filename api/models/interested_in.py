from api import db

# N:N 
Interested_in = db.Table('interested_in', 
                db.Column('consumer_id', db.Integer, db.ForeignKey('consumer.id', ondelete='CASCADE')),
                db.Column('topic_id', db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'))
)