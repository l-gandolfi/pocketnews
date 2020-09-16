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

class TestAdminUsers_list(unittest.TestCase):

    #Class for test /admin/users backend path.
    #In particular, we are going to test if results are correct.

    tester = app.test_client()
    
    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "email_1_test_back",
        "username": "user1",
        "password": "password_1",
    }
    
    consumer_2 = {
        "name": "name_2",
        "surname": "last_name_2",
        "email": "email_2_test_back",
        "username": "user2",
        "password": "password_2",
    }    
    
    topics_consumer_1 = {
        "topics": [
            {
            'topic': 'topic_8',
            'id': 1007
            },
            {
            'topic': 'topic_1',
            'id': 1000
            },
            {
            'topic': 'topic_4',
            'id': 1003
            },
            {
            'topic': 'topic_2',
            'id': 1001
            }
        ],
        'user_id': ''
    }
    

    def setUp(self):

        #Let's think this test as independent: we have to populate the database with topics.
        #Then we have to register one or more users.
        #When this operation will be automatized using docker, just comment the next method call.

        self.populate_topics()
        # self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
        hashed_password = generate_password_hash(self.consumer_1['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_1['name'], surname=self.consumer_1['surname'], email=self.consumer_1['email'], username=self.consumer_1['username'], password=hashed_password, email_checked=False, reset_done=False)

        db.session.add(consumer)
        db.session.commit()
        
        consumer = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        consumer.email_checked = True
        db.session.commit()

        self.topics_consumer_1['user_id'] = consumer.id

    
        # self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), content_type='application/json', follow_redirects=True)  
        hashed_password = generate_password_hash(self.consumer_2['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_2['name'], surname=self.consumer_2['surname'], email=self.consumer_2['email'], username=self.consumer_2['username'], password=hashed_password, email_checked=False, reset_done=False)

        db.session.add(consumer)
        db.session.commit()

        consumer = Consumer.query.filter_by(email=self.consumer_2['email']).first()
        consumer.email_checked = True
        db.session.commit()         
   
    def test_get(self):
        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }
        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer_1), content_type='application/json', follow_redirects=True, headers=self.header)
        response = self.tester.get('http://localhost:5000/admin/users', content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))

        self.assertEqual(response_json['status'], 'success')
        users_check = ["user1", "user2"]
        index = 0
        db_usernames = set()
        for user in response_json['usernames']:
            db_usernames.add(user['username'])
        for user in users_check:
            self.assertTrue(user in db_usernames)
    
    def test_post(self):
        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }
        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer_1), content_type='application/json', follow_redirects=True, headers=self.header)
        payload = {'username': self.consumer_1['username']}
        response = self.tester.post('http://localhost:5000/admin/users', data = json.dumps(payload), content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['name'], self.consumer_1['name'])
        self.assertEqual(response_json['surname'], self.consumer_1['surname'])
        self.assertEqual(response_json['email'], self.consumer_1['email'])
        
        topic_list = []
        for topic in self.topics_consumer_1['topics']:
            topic_list.append(topic['topic'])
        self.assertEqual(set(response_json['topics']), set(topic_list))
        
        payload = {'username': self.consumer_2['username']}
        response = self.tester.post('http://localhost:5000/admin/users', data = json.dumps(payload), content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['name'], self.consumer_2['name'])
        self.assertEqual(response_json['surname'], self.consumer_2['surname'])
        self.assertEqual(response_json['email'], self.consumer_2['email'])
        
        self.assertEqual(response_json['topics'], [])
        
    def tearDown(self):
        # Delete consumers added
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        cons_2 = Consumer.query.filter_by(email=self.consumer_2['email']).first()

        if cons_1:
            db.session.delete(cons_1)

        if cons_2:
            db.session.delete(cons_2)
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
