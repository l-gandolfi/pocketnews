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

class TestModifyPublicProfileStory(unittest.TestCase):

    tester = app.test_client()

    consumer_1 = {
          "name": "name_1",
          "surname": "last_name_1",
          "email": "email_1_test_back",
          "username": "username_1",
          "password": "password_1",
          "confirmpassword": "password_1",
    }

    consumer_1_info = {
        "city": "city_1",
        "bio": "bio_1",
        "dob": "dob_1",
        "topics": "topic_1, topic_2",
        "publicinfo": "11111"
    }

    consumer_2 = {
          "name": "name_2",
          "surname": "last_name_2",
          "email": "email_2_test_back",
          "username": "username_2",
          "password": "password_2",
          "confirmpassword": "password_2",
    }

    consumer_2_info = {
        "city": "city_2",
        "bio": "bio_2",
        "dob": "dob_2",
        "topics": "topic_1, topic_3",
        "publicinfo": "11110"        
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

    topics_consumer_2 = {
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
        consumer =  Consumer.query.filter_by(email=self.consumer_1['email']).first()
        consumer.email_checked = True
        self.topics_consumer['user_id'] = consumer.id
        db.session.commit()

        hashed_password = generate_password_hash(self.consumer_2['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_2['name'], surname=self.consumer_2['surname'], email=self.consumer_2['email'], username=self.consumer_2['username'], password=hashed_password, email_checked=True, reset_done=False)
        db.session.add(consumer)
        db.session.commit()
        consumer =  Consumer.query.filter_by(email=self.consumer_2['email']).first()
        consumer.email_checked = True
        self.topics_consumer_2['user_id'] = consumer.id
        db.session.commit()


    def test_correct_modify_profile(self):
        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1),
        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer), content_type='application/json', follow_redirects=True, headers=self.header)
        
        response = self.tester.post('http://localhost:5000/modifypublicprofile', data = json.dumps(self.consumer_1_info), 
                                        content_type='application/json', follow_redirects=True, headers=self.header)
                                       
        response_json = ast.literal_eval(response.data.decode('utf-8')) 
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['information']['city'], self.consumer_1_info['city'])
        self.assertEqual(response_json['information']['bio'], self.consumer_1_info['bio'])
        self.assertEqual(response_json['information']['dob'], self.consumer_1_info['dob'])
        self.assertEqual(response_json['information']['publicinfo'], self.consumer_1_info['publicinfo'])

        response_json = ast.literal_eval(response.data.decode('utf-8'))
        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_2),
        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer_2), content_type='application/json', follow_redirects=True, headers=self.header)

        response = self.tester.post('http://localhost:5000/modifypublicprofile', data = json.dumps(self.consumer_2_info), 
                                        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['information']['city'], self.consumer_2_info['city'])
        self.assertEqual(response_json['information']['bio'], self.consumer_2_info['bio'])
        self.assertEqual(response_json['information']['dob'], self.consumer_2_info['dob'])
        self.assertEqual(response_json['information']['publicinfo'], self.consumer_2_info['publicinfo'])
        self.tester.get('http://localhost:5000/logout')

    def tearDown(self):
        cons_1 = Consumer.query.filter_by(username=self.consumer_1['username']).first()
        cons_2 = Consumer.query.filter_by(username=self.consumer_2['username']).first()

        if cons_1:
            db.session.delete(cons_1)

        if cons_2:
            db.session.delete(cons_2)

        db.session.commit()


