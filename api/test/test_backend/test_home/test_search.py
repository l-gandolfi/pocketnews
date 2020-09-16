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

class TestSearchUsersStory(unittest.TestCase):

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

    consumer_3 = {
          "name": "name_3",
          "surname": "last_name_3",
          "email": "email_3_test_back",
          "username": "username_3",
          "password": "password_3",
          "confirmpassword": "password_3",
    }
    def setUp(self):
        hashed_password = generate_password_hash(self.consumer_1['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_1['name'], surname=self.consumer_1['surname'], email=self.consumer_1['email'], username=self.consumer_1['username'], password=hashed_password, email_checked=False, reset_done=False)
        db.session.add(consumer)
        db.session.commit()

        hashed_password = generate_password_hash(self.consumer_2['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_2['name'], surname=self.consumer_2['surname'], email=self.consumer_2['email'], username=self.consumer_2['username'], password=hashed_password, email_checked=False, reset_done=False)
        db.session.add(consumer)
        db.session.commit()

        hashed_password = generate_password_hash(self.consumer_3['password']).decode('utf-8')
        consumer = Consumer(name=self.consumer_3['name'], surname=self.consumer_3['surname'], email=self.consumer_3['email'], username=self.consumer_3['username'], password=hashed_password, email_checked=False, reset_done=False)
        db.session.add(consumer)
        db.session.commit()


    def test_search_users(self):

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1), 
        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))

        response = self.tester.get('http://localhost:5000/search?username='+'username', data = json.dumps(self.consumer_1), 
            content_type='application/json', follow_redirects=True)
                                       
        response_json = ast.literal_eval(response.data.decode('utf-8')) 
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(self.consumer_1['username'] in response_json['usernames'], True)
        self.assertEqual(self.consumer_2['username'] in response_json['usernames'], True)
        self.assertEqual(self.consumer_3['username'] in response_json['usernames'], True)

        response = self.tester.get('http://localhost:5000/search?username='+'username_1', data = json.dumps(self.consumer_1), 
            content_type='application/json', follow_redirects=True)
                                       
        response_json = ast.literal_eval(response.data.decode('utf-8')) 
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['usernames'], [self.consumer_1['username']])

        response = self.tester.get('http://localhost:5000/search?username='+'utente', data = json.dumps(self.consumer_1), 
            content_type='application/json', follow_redirects=True)
                                       
        response_json = ast.literal_eval(response.data.decode('utf-8')) 
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['usernames'], [])
        self.tester.get('http://localhost:5000/logout')

    def tearDown(self):
        cons_1 = Consumer.query.filter_by(username=self.consumer_1['username']).first()
        cons_2 = Consumer.query.filter_by(username=self.consumer_2['username']).first()
        cons_3 = Consumer.query.filter_by(username=self.consumer_3['username']).first()

        if cons_1:
            db.session.delete(cons_1)

        if cons_2:
            db.session.delete(cons_2)

        if cons_3:
            db.session.delete(cons_3)
            
        db.session.commit()
