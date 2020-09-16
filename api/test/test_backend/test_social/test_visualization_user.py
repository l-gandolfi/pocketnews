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

class TestVisualizationUserStory(unittest.TestCase):
    

    tester = app.test_client()

    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "email_1_test_back",
        "username": "username_1",
        "password": "password_1",
        "confirmpassword": "password_1",
    }

    consumer_2 = {
        "name": "name_2",
        "surname": "last_name_2",
        "email": "email_2_test_back",
        "username": "username_2",
        "password": "password_2",
        "confirmpassword": "password_2",
    }

    consumer_1_info = {
        "city": "city_1",
        "bio": "bio_1",
        "dob": "dob_1",
        "publicinfo": "11110",
    }

    consumer_2_info = {
        "city": 'city_2',
        "bio": "bio_2",
        "dob": "dob_2",
        "publicinfo": "00010",
    }

    def setUp(self):
        hashed_password = generate_password_hash(self.consumer_1['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_1['name'], surname=self.consumer_1['surname'], email=self.consumer_1['email'], username=self.consumer_1['username'], password=hashed_password, email_checked=True, reset_done=False)
        db.session.add(consumer)
        db.session.commit()
        consumer =  Consumer.query.filter_by(email=self.consumer_1['email']).first()
        consumer.email_checked = True

        db.session.commit()

        hashed_password = generate_password_hash(self.consumer_2['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_2['name'], surname=self.consumer_2['surname'], email=self.consumer_2['email'], username=self.consumer_2['username'], password=hashed_password, email_checked=True, reset_done=False)
        db.session.add(consumer)
        db.session.commit()
        consumer =  Consumer.query.filter_by(email=self.consumer_2['email']).first()
        consumer.email_checked = True

        db.session.commit()

    def test_correct_users_Visualization(self):


        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1),
        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        response = self.tester.post('http://localhost:5000/modifypublicprofile', data = json.dumps(self.consumer_1_info), content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        user_id = Consumer.query.filter_by(email=self.consumer_1['email']).first().id

        response = self.tester.get('http://localhost:5000/profile?username='+ self.consumer_1['username'], data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json["information"]["first_name"], self.consumer_1['name'])
        self.assertEqual(response_json["information"]["last_name"], self.consumer_1['surname'])
        self.assertEqual(response_json["information"]["email"], self.consumer_1['email'])
        self.assertEqual(response_json["information"]["username"], self.consumer_1['username'])
        self.assertEqual(response_json["information"]["city"], self.consumer_1_info['city'])
        self.assertEqual(response_json["information"]["bio"], self.consumer_1_info['bio'])
        self.assertEqual(response_json["information"]["dob"], self.consumer_1_info['dob'])
        self.assertEqual(response_json["information"]["publicinfo"], self.consumer_1_info['publicinfo'])

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_2),
        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }
        self.tester.post('http://localhost:5000/modifypublicprofile', data = json.dumps(self.consumer_2_info), content_type='application/json', follow_redirects=True, headers=self.header)

        response = self.tester.get('http://localhost:5000/profile?username='+ self.consumer_2['username'], data = json.dumps(self.consumer_2), 
                                        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json["information"]["first_name"], self.consumer_2['name'])
        self.assertEqual(response_json["information"]["last_name"], self.consumer_2['surname'])
        self.assertEqual(response_json["information"]["email"], self.consumer_2['email'])
        self.assertEqual(response_json["information"]["username"], self.consumer_2['username'])
        self.assertEqual(response_json["information"]["city"], self.consumer_2_info['city'])
        self.assertEqual(response_json["information"]["bio"], self.consumer_2_info['bio'])
        self.assertEqual(response_json["information"]["dob"], self.consumer_2_info['dob'])
        self.assertEqual(response_json["information"]["publicinfo"], self.consumer_2_info['publicinfo'])

        response = self.tester.get('http://localhost:5000/profile?username=agata', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response_json['status'], 'fail')

    def tearDown(self):
        cons_1 = Consumer.query.filter_by(username=self.consumer_1['username']).first()
        cons_2 = Consumer.query.filter_by(username=self.consumer_2['username']).first()

        if cons_1:
            db.session.delete(cons_1)

        if cons_2:
            db.session.delete(cons_2)

        db.session.commit()


