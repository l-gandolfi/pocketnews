from api import app, db
from models import *
from sqlalchemy import desc
import unittest
import json
import ast
import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

from models.consumer import *
from models.interested_in import *
from models.like import *
from models.news import *
from models.recommended import *
from models.topic import *

class TestTopicSelectionStory(unittest.TestCase):

    #Class for testing /topics route backend.

    tester = app.test_client()

    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "email_1_test_back",
        "username": "user1",
        "password": "password_1",
        "id": ""
    }
    
    topics_consumer_1 = {
        "topics": [
            {
            'topic': 'topic_1',
            'id': 1000
            },
            {
            'topic': 'topic_2',
            'id': 1001
            },
            {
            'topic': 'topic_4',
            'id': 1003
            },
            {
            'topic': 'topic_8',
            'id': 1007
            }
        ],
        "user_id": ''
    }
    
    header = None

    def setUp(self):

        #Let's think this test as independent: we have to populate the database with topics.
        #When this operation will be automatized using docker, just comment the next method call.

        self.populate_topics()
        hashed_password = generate_password_hash(self.consumer_1['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_1['name'], surname=self.consumer_1['surname'], email=self.consumer_1['email'], username=self.consumer_1['username'], password=hashed_password, email_checked=False, reset_done=False)

        db.session.add(consumer)
        db.session.commit()

    def test_db_save(self):

        self.set_mail_checked()
        # Assign topics
        user_id = Consumer.query.filter_by(email=self.consumer_1['email']).first().id
        self.topics_consumer_1['user_id'] = user_id

        response = self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer_1), content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))

        self.assertEqual(response_json['status'], 'success')
        
        # Query
        consumer_1 = Consumer.query.filter_by(username=self.consumer_1['username']).first()
        
        topic_values=[t['id'] for t in self.topics_consumer_1['topics']]
        
        # Test values
        counter = 0
        for topic in consumer_1.interested:
            self.assertEqual(topic.id, topic_values[counter])
            counter += 1

    def tearDown(self):
        # Delete consumer added
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        db.session.delete(cons_1)
        db.session.commit()
        
        # Delete topic added
        topics = Topic.query.order_by(desc(Topic.id)).limit(11)
        for topic in topics:
            db.session.delete(topic)
        db.session.commit()
        
        
    def populate_topics(self):
        topics_list = ['topic_1', 'topic_2', 'topic_3', 'topic_4', 'topic_5', 'topic_6', 'topic_7', 'topic_8', 'topic_9', 'topic_10', 'topic_11']
        index = 1000
        for topic in topics_list:
            db.session.add(Topic(id=index, topic=topic))
            index += 1
        db.session.commit()
    
    def set_mail_checked(self):
        consumer = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        consumer.email_checked = True
        db.session.commit()
        
        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        } 
