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

class TestHomeView(unittest.TestCase):
    tester = app.test_client()
    
    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "email_1_test_back",
        "username": "user1",
        "password": "password_1",
    }
    
    topics_consumer_1 = {
        "topics": [
            {
            'topic': 'music',
            'id': 0
            },
            {
            'topic': 'science',
            'id': 1
            }
        ],
        "user_id": ""
    }
    
    def setUp(self):
        
        hashed_password = generate_password_hash(self.consumer_1['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_1['name'], surname=self.consumer_1['surname'], email=self.consumer_1['email'], username=self.consumer_1['username'], password=hashed_password, email_checked=True, reset_done=False)
        db.session.add(consumer)
        db.session.commit()
        consumer =  Consumer.query.filter_by(email=self.consumer_1['email']).first()
        consumer.email_checked = True
        db.session.commit()

        self.topics_consumer_1['user_id'] = consumer.id

    def test_get_feed(self):
        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer_1), content_type='application/json', follow_redirects=True, headers=self.header)

        response = self.tester.get('http://localhost:5000/feed', headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(len(response_json['data']), 10)
    
    def tearDown(self):
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        db.session.delete(cons_1)
        db.session.commit()


