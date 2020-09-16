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

app.testing = True

class TestRegistrationStory(unittest.TestCase):

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

    consumer_3 = {
          "name": "name_3",
          "surname": "last_name_3",
          "email": "email_2_test_back",
          "username": "username_3",
          "password": "password_2",
    }
    consumer_4 = {
          "name": "name_4",
          "surname": "last_name_4",
          "email": "email_4_test_back",
          "username": "username_2",
          "password": "password_4",
    }

    tester = app.test_client()
 
    def test_correct_users_registration(self):

        response = self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['reason'], '')
        consumer_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        self.assertEqual(consumer_1.name, 'name_1')
        self.assertEqual(consumer_1.surname, 'last_name_1')
        self.assertEqual(consumer_1.username, 'username_1')
        self.assertEqual(check_password_hash(consumer_1.password, 'password_1'), True)
        self.assertEqual(consumer_1.email_checked, False)

        response = self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['reason'], '')
        consumer_2 = Consumer.query.filter_by(email=self.consumer_2['email']).first()
        self.assertEqual(consumer_2.name, 'name_2')
        self.assertEqual(consumer_2.surname, 'last_name_2')
        self.assertEqual(consumer_2.username, 'username_2')
        self.assertEqual(check_password_hash(consumer_2.password, 'password_2'), True)
        self.assertEqual(consumer_2.email_checked, False)

    def test_already_used_email(self):
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), 
                                        content_type='application/json', follow_redirects=True)

        response = self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_3), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['reason'], 'email')

    def test_wait_confirm(self):
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)

        consumer_id = Consumer.query.filter_by(email=self.consumer_1['email']).first().id

        payload = {
          'user_id': consumer_id,
          'op_id': 1,
        }

        response = self.tester.post('http://localhost:5000/mail_checked', data = json.dumps(payload), content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))

        self.assertEqual(response_json['status'], '12')
        self.assertEqual(response_json['message'], 'Email doesn\'t checked')

        response = self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)

    
    def test_already_used_username(self):
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), 
                                        content_type='application/json', follow_redirects=True)

        response = self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_4), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['reason'], 'username')

    def tearDown(self):
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        cons_2 = Consumer.query.filter_by(email=self.consumer_2['email']).first()
        
        if cons_1:
            db.session.delete(cons_1)
        if cons_2:
            db.session.delete(cons_2)

        db.session.commit()
