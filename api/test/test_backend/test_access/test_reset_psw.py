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

class TestPasswordReset(unittest.TestCase):
    tester = app.test_client()

    consumer_1 = {
          "name": "name_1",
          "surname": "last_name_1",
          "email": "email_1_test_back",
          "username": "username_1",
          "password": "password_1",
          "confirmpassword": "password_1",
    }

    consumer_id = ''
    
    payload_request = {
        'email': consumer_1['email'],
        'op_id': 0,
    }

    payload_request_wrong_email = {
        'email': 'wrong_email_test_back',
        'op_id': 0,
    }

    payload_access_reset = {
        'user_id': '',
        'op_id': 2,
    }

    payload_send_new_password = {
        'user_id': '',
        'password': 'new_password',
        'op_id': 1,
    }
    

    def setUp(self):
        
        # self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
        hashed_password = generate_password_hash(self.consumer_1['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_1['name'], surname=self.consumer_1['surname'], email=self.consumer_1['email'], username=self.consumer_1['username'], password=hashed_password, email_checked=False, reset_done=False)

        db.session.add(consumer)
        db.session.commit()
        
        self.consumer_id = Consumer.query.filter_by(username=self.consumer_1['username']).first().id

        self.payload_access_reset['user_id'] = self.consumer_id
        self.payload_send_new_password['user_id'] = self.consumer_id

    def test_correct_reset_password(self):


        response = self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_request), content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8')) 

        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['reason'], '')

        response = self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_access_reset), content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8')) 

        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['reason'], '')


        response = self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_send_new_password), content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8')) 

        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['reason'], '')

    def test_wrong_email_reset_psw(self):

        response = self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_request_wrong_email), content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8')) 

        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['reason'], 'No user with that email')
    
    def test_multiple_reset_psw(self):

        self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_request), content_type='application/json', follow_redirects=True)
        self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_access_reset), content_type='application/json', follow_redirects=True)
        self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_send_new_password), content_type='application/json', follow_redirects=True)
        response = self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_send_new_password), content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8')) 

        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['reason'], 'change already done') 

    def test_request_expired_time(self):

        self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_request), content_type='application/json', follow_redirects=True)
        consumer = Consumer.query.filter_by(username=self.consumer_1['username']).first()
        new_reset_psw_data = consumer.reset_psw_date - datetime.timedelta(seconds=260)
        consumer.reset_psw_date = new_reset_psw_data
        db.session.commit()

        response = self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_access_reset), content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8')) 

        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['reason'], 'request expired') 

    def tearDown(self):
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        
        if cons_1:
            db.session.delete(cons_1)


        db.session.commit()

