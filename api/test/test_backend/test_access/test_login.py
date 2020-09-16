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

class TestLoginStory(unittest.TestCase):

    tester = app.test_client()

    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "email_1_test_back",
        "username": "user1",
        "password": "password_1",
    }

    topics_consumer = {
    "topics": [
        {
        'topic': 'tech',
        'id': 0
        },
        {
        'topic': 'cinema',
        'id': 1
        }
    ],
    "user_id": ""
    }

    
    def setUp(self):
        # self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
        hashed_password = generate_password_hash(self.consumer_1['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_1['name'], surname=self.consumer_1['surname'], email=self.consumer_1['email'], username=self.consumer_1['username'], password=hashed_password, email_checked=False, reset_done=False)
        db.session.add(consumer)
        db.session.commit()

    def test_correct_users_login_no_conf(self):
        payload = {
            "email": self.consumer_1['email'],
            "password": "password_1",
            "remember_flag": True
        }

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(payload), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'warning')
        self.assertEqual(response_json['reason'], 'Email no checked')

    def test_correct_users_login_yes_conf(self):
        consumer =  Consumer.query.filter_by(email=self.consumer_1['email']).first()
        consumer.email_checked = True
        db.session.commit()

        payload = {
            "email": self.consumer_1['email'],
            "password": "password_1",
            "remember_flag": True
        }

        self.topics_consumer['user_id'] = consumer.id
        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer), content_type='application/json', follow_redirects=True)

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(payload), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['reason'], '')

    def test_wrong_email_login(self):
        payload = {
            "email": "email_1_wrong",
            "password": "password_1",
            "remember_flag": True
        }

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(payload), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['reason'], 'Wrong email or password')

    def test_wrong_password_login(self):
        payload = {
            "email": "email_1",
            "password": "password_1_wrong",
            "remember_flag": True
        }

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(payload), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['reason'], 'Wrong email or password')

    def tearDown(self):
        delete_consumer_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()

        if delete_consumer_1:
            db.session.delete(delete_consumer_1)

        db.session.commit()
