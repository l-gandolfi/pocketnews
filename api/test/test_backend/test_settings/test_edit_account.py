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


class TestEditAccountInformationStory(unittest.TestCase):

    tester = app.test_client()

    consumer_1 = {
        "name": "name_1",
        "surname":"last_name1",
        "email": "email_1_test_back@gmail.com",
        "username": "user_1",
        "password": "password_1"
    }

    consumer_2 = {
        "name": "name_2",
        "surname":"last_name2",
        "email": "email_2_test_back@gmail.com",
        "username": "user_2",
        "password": "password_2",
    }
    
    changes_consumer_1 = {
        "name": "changes_name_1",
        "surname":"changes_last_name1",
        "email": "changes_email_1_test_back@gmail.com",
        "username": "changes_user_1",
        "password": "changes_password_1",
        "confirmpassword": "changes_password_1",
    }

    # Username already taken
    changes_consumer_2_1 = {
        "name": "name_2",
        "surname":"last_name2",
        "email": "email_2_test_back@gmail.com",
        "username": "changes_user_1",
        "password": "password_2",
        "confirmpassword": "password_2",
    }
    
    # Email already taken
    changes_consumer_2_2= {
        "name": "name_2",
        "surname":"last_name2",
        "email": "changes_email_1_test_back@gmail.com",
        "username": "user_2",
        "password": "password_2",
        "confirmpassword": "password_2",
    }

    # Wrong password
    changes_consumer_2_3= {
        "name": "name_2",
        "surname":"last_name2",
        "email": "email_2_test_back@gmail.com",
        "username": "user_2",
        "password": "password_2",
        "confirmpassword": "wrong_password_2",
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
        hashed_password = generate_password_hash(self.consumer_1['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_1['name'], surname=self.consumer_1['surname'], email=self.consumer_1['email'], username=self.consumer_1['username'], password=hashed_password, email_checked=True, reset_done=False)
        db.session.add(consumer)
        db.session.commit()

        consumer = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        consumer.email_checked = True
        db.session.commit()
        self.topics_consumer['user_id'] = consumer.id

        hashed_password = generate_password_hash(self.consumer_2['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_2['name'], surname=self.consumer_2['surname'], email=self.consumer_2['email'], username=self.consumer_2['username'], password=hashed_password, email_checked=True, reset_done=False)
        db.session.add(consumer)
        db.session.commit()

        consumer =  Consumer.query.filter_by(email=self.consumer_2['email']).first()
        consumer.email_checked = True
        db.session.commit()
        self.topics_consumer['user_id'] = consumer.id
        
    def test_edit_user_information(self):

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }
        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer), content_type='application/json', follow_redirects=True, headers=self.header)

        # Changes in user_1 information 
        response = self.tester.post('http://localhost:5000/editaccount', data = json.dumps(self.changes_consumer_1), 
        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        # Changes didn't raise any exception
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['reason'], '')

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_2), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer), content_type='application/json', follow_redirects=True, headers=self.header)

        # Changes in user_2 information (Username already taken)
        response = self.tester.post('http://localhost:5000/editaccount', data = json.dumps(self.changes_consumer_2_1), 
        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        # Changes rejected
        self.assertEqual(response_json['status'], 'fail')
        # Changes raised user or email already taken
        self.assertEqual(response_json['reason'], 'Username already taken.')

        # Changes in user_2 information (Email already taken)
        response = self.tester.post('http://localhost:5000/editaccount', data = json.dumps(self.changes_consumer_2_2), 
        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        # Changes rejected
        self.assertEqual(response_json['status'], 'fail')
        # Changes raised user or email already taken
        self.assertEqual(response_json['reason'], 'Email already taken.')

        # Changes in user_2 information (Wrong confirmation password)
        response = self.tester.post('http://localhost:5000/editaccount', data = json.dumps(self.changes_consumer_2_3), 
        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        # Changes rejected
        self.assertEqual(response_json['status'], 'fail')
        # Changes raised user or email already taken
        self.assertEqual(response_json['reason'], "Password and Confirmation Password don't match.")

    def tearDown(self):
        # Retrieving consumers registered to test functionalities

        consumer_1 = Consumer.query.filter_by(username=self.changes_consumer_1['username']).first()

        db.session.delete(consumer_1)
        db.session.commit()

        consumer_2 = Consumer.query.filter_by(username=self.consumer_2['username']).first()
        
        db.session.delete(consumer_2)
        db.session.commit()
