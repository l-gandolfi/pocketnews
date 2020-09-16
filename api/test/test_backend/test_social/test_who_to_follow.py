import ast
import datetime
import json
import unittest

from api import app, db
from flask_bcrypt import check_password_hash, generate_password_hash
from models import *
from models.consumer import *
from models.interested_in import *
from models.like import *
from models.news import *
from models.recommended import *
from models.topic import *
from sqlalchemy import desc

app.testing = True

class TestWhoToFollow(unittest.TestCase):
    
    tester = app.test_client()
    
    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "email_1@test_backend.it",
        "username": "user1",
        "password": "password_1",
    }
    
    topics_consumer_1 = {
        "topics": [
            {
            'topic': 'topic_1',
            'id': 1001
            },
            {
            'topic': 'topic_2',
            'id': 1002
            }
        ],
        "user_id": ""
    }
    
    consumer_2 = {
        "name": "name_2",
        "surname": "last_name_2",
        "email": "email_2@test_backend.it",
        "username": "user2",
        "password": "password_2",
    }
    
    topics_consumer_2 = {
        "topics": [
            {
            'topic': 'topic_1',
            'id': 1001
            },
            {
            'topic': 'topic_3',
            'id': 1003
            }
        ],
        "user_id": ""
    }
    
    consumer_3 = {
        "name": "name_3",
        "surname": "last_name_3",
        "email": "email_3@test_backend.it",
        "username": "user3",
        "password": "password_3",
    }
    
    topics_consumer_3 = {
        "topics": [
            {
            'topic': 'topic_1',
            'id': 1001
            },
            {
            'topic': 'topic_3',
            'id': 1002
            }
        ],
        "user_id": ""
    }
    
    consumer_4 = {
        "name": "name_4",
        "surname": "last_name_4",
        "email": "email_4@test_backend.it",
        "username": "user4",
        "password": "password_4",
    }
    
    topics_consumer_4 = {
        "topics": [
            {
            'topic': 'topic_1',
            'id': 1003
            },
            {
            'topic': 'topic_3',
            'id': 1004
            }
        ],
        "user_id": ""
    }
    
    def setUp(self):
        self.populate_topics()
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
        consumer =  Consumer.query.filter_by(email=self.consumer_1['email']).first()
        consumer.email_checked = True
        db.session.commit()

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.topics_consumer_1['user_id'] = consumer.id
        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer_1), content_type='application/json', follow_redirects=True, headers=self.header)
    
    def test_single_suggestion(self):
        # Register another user and login to set topics and complete registration
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), content_type='application/json', follow_redirects=True)
        consumer =  Consumer.query.filter_by(email=self.consumer_2['email']).first()
        consumer.email_checked = True
        db.session.commit()

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_2), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.topics_consumer_2['user_id'] = consumer.id
        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer_2), content_type='application/json', follow_redirects=True, headers=self.header)
        
        # Check results now, list should have len = 1 and contains the right data
        response = self.tester.get('http://localhost:5000/social/who-to-follow', headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(len(response_json['data']), 1)
        consumer_suggested =  Consumer.query.filter_by(email=self.consumer_1['email']).first()
        self.assertEqual(response_json['data'], [consumer_suggested.to_json()])
    
    def test_no_suggestions(self):
        # Only consumer 1 registered -> the results is an empty list
        response = self.tester.get('http://localhost:5000/social/who-to-follow', headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['data'], [])
        
    def test_multiple_suggestions(self):
        # Register another 3 users and login them to set topics and complete registration
        # 1. The first user to be registered is a user with no topics related to our testing user
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_4), content_type='application/json', follow_redirects=True)
        consumer =  Consumer.query.filter_by(email=self.consumer_4['email']).first()
        consumer.email_checked = True
        db.session.commit()

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_4), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.topics_consumer_4['user_id'] = consumer.id
        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer_4), content_type='application/json', follow_redirects=True, headers=self.header)
        
        # 2.
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), content_type='application/json', follow_redirects=True)
        consumer =  Consumer.query.filter_by(email=self.consumer_2['email']).first()
        consumer.email_checked = True
        db.session.commit()

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_2), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.topics_consumer_2['user_id'] = consumer.id
        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer_2), content_type='application/json', follow_redirects=True, headers=self.header)
        
        # 3.
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_3), content_type='application/json', follow_redirects=True)
        consumer =  Consumer.query.filter_by(email=self.consumer_3['email']).first()
        consumer.email_checked = True
        db.session.commit()

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_3), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.topics_consumer_3['user_id'] = consumer.id
        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer_3), content_type='application/json', follow_redirects=True, headers=self.header)
        
        # Now control results: current user is 3.
        response = self.tester.get('http://localhost:5000/social/who-to-follow', headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(len(response_json['data']), 2)
        consumer1_suggested =  Consumer.query.filter_by(email=self.consumer_1['email']).first()
        consumer2_suggested =  Consumer.query.filter_by(email=self.consumer_2['email']).first()
        self.assertEqual(response_json['data'], [consumer1_suggested.to_json(), consumer2_suggested.to_json()])
       
    def tearDown(self):
        # Delete users created
        cons_1 = Consumer.query.filter_by(username=self.consumer_1['username']).first()
        cons_2 = Consumer.query.filter_by(username=self.consumer_2['username']).first()
        cons_3 = Consumer.query.filter_by(username=self.consumer_3['username']).first()
        cons_4 = Consumer.query.filter_by(username=self.consumer_4['username']).first()
        if cons_1:
            db.session.delete(cons_1)
        if cons_2:
            db.session.delete(cons_2)
        if cons_3:
            db.session.delete(cons_3)
        if cons_4:
            db.session.delete(cons_4)
        # Delete topic added
        topics = Topic.query.order_by(desc(Topic.id)).limit(4)
        for topic in topics:
            db.session.delete(topic)
        db.session.commit() 

    
    def populate_topics(self):
        topics_list = ['topic_1', 'topic_2', 'topic_3', 'topic_4']
        index = 1001
        for topic in topics_list:
            db.session.add(Topic(id=index, topic=topic))
            index += 1
        db.session.commit()    

if __name__ == '__main__':
    unittest.main()
