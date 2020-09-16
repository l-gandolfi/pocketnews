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


class TestResendConfirmEmail(unittest.TestCase):
    consumer_1 = {
          "name": "name_1",
          "surname": "last_name_1",
          "email": "email_1_test_back",
          "username": "username_1",
          "password": "password_1",
    }

    consumer_2 = {
          "name": "name_2",
          "surname": "last_name_2",
          "email": "email_2_test_back",
          "username": "username_2",
          "password": "password_2",
    }

    correct_payload = {
        "email": 'email_new_test_back',
        "user_id": ""
    }

    wrong_payload = {
        "email": consumer_1['email'],
        "user_id": ""
    }

    user_id_1 = ""
    user_id_2 = ""

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

    tester = app.test_client()

    def setUp(self):
        #self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
        #self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), content_type='application/json', follow_redirects=True)

        hashed_password = generate_password_hash(self.consumer_1['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_1['name'], surname=self.consumer_1['surname'], email=self.consumer_1['email'], username=self.consumer_1['username'], password=hashed_password, email_checked=False, reset_done=False)

        db.session.add(consumer)
        db.session.commit()

        hashed_password = generate_password_hash(self.consumer_2['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_2['name'], surname=self.consumer_2['surname'], email=self.consumer_2['email'], username=self.consumer_2['username'], password=hashed_password, email_checked=False, reset_done=False)
        
        db.session.add(consumer)
        db.session.commit()

        consumer = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        self.user_id_1 = consumer.id

        consumer = Consumer.query.filter_by(email=self.consumer_2['email']).first()
        self.user_id_2 = consumer.id

    def test_correct_change(self):
        self.correct_payload['user_id'] = self.user_id_1
        response = self.tester.post('http://localhost:5000/resend_email', data = json.dumps(self.correct_payload), content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))

        self.assertEqual(response_json['status'], 'success')

        consumer = Consumer.query.filter_by(id=self.user_id_1).first()

        self.assertEqual(consumer.email, 'email_new_test_back')

    def test_wrong_change(self):
        self.wrong_payload['user_id'] = self.user_id_2
        response = self.tester.post('http://localhost:5000/resend_email', data = json.dumps(self.wrong_payload), content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))

        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['reason'], 'Email already used!')

        consumer = Consumer.query.filter_by(id=self.user_id_2).first()

        self.assertEqual(consumer.email, self.consumer_2['email'])

    def test_resend_block(self):

        self.correct_payload['user_id'] = self.user_id_1
        self.topics_consumer['user_id'] = self.user_id_1
        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer), content_type='application/json', follow_redirects=True) 

        consumer = Consumer.query.filter_by(id=self.user_id_1).first()
        consumer.email_checked = True
        db.session.commit()

        response = self.tester.post('http://localhost:5000/resend_email', data = json.dumps(self.correct_payload), content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))

        self.assertEqual(response_json['status'], 'warning')
        self.assertEqual(response_json['reason'], 'Email already checked!')

    def tearDown(self):
        cons_1 = Consumer.query.filter_by(id=self.user_id_1).first()
        cons_2 = Consumer.query.filter_by(id=self.user_id_2).first()
        if cons_1:
            db.session.delete(cons_1)
        if cons_2:
            db.session.delete(cons_2)

        db.session.commit()      

