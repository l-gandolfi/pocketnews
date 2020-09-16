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

app.testing = True

class TestTopicSettingsStory(unittest.TestCase):

    tester = app.test_client()

    consumer_1 = {
        "name": "name_1",
        "surname":"last_name1",
        "email": "email_1@gmail.com",
        "username": "user_1",
        "password": "password_1"
    }

    topics_consumer = {
    "topics": [
        {
        'topic': 'cinema',
        'id': 0
        },
        {
        'topic': 'economics',
        'id': 1
        }
    ],
    "user_id": ""
    }

    adding_topics_consumer = {
    "topics": [
        {"topic": "Cinema", 
        "id": 0
        }, 
        {"topic": "Economics", 
        "id": 1
        }, 
        {"topic": "Environment", 
        "id": 2
        }
        ]
    } 

    removing_topics_consumer = {
    "topics": [
        {"topic": "Economics", 
        "id": 0
        }, 
        {"topic": "Environment", 
        "id": 2
        }
        ]
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
      
    def test_edit_topic_information(self):
        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))

        
        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer), 
        content_type='application/json', follow_redirects=True, headers=self.header)
        # Getting consumer_1 preferred topics
        response = self.tester.get('http://localhost:5000/settings/topics', content_type='application/json',
        follow_redirects=True, headers=self.header)
        response_json = json.loads(response.data)

        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['topics'][0]['topic'], "Cinema")
        self.assertEqual(response_json['topics'][0]['clicked'], True)
        self.assertEqual(response_json['topics'][1]['topic'], "Economics")
        self.assertEqual(response_json['topics'][1]['clicked'], True)

        # Adding topics to consumer_1 preferences
        response = self.tester.post('http://localhost:5000/settings/topics', data = json.dumps(self.adding_topics_consumer), 
        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = json.loads(response.data)

        # Checking consumer_1 topics update
        self.assertEqual(response_json['status'], 'success')
        
        response = self.tester.get('http://localhost:5000/settings/topics', content_type='application/json',
        follow_redirects=True, headers=self.header)
        response_json = json.loads(response.data)

        # Changes didn't raise any exception
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['topics'][0]['topic'], "Cinema")
        self.assertEqual(response_json['topics'][0]['clicked'], True)

        self.assertEqual(response_json['topics'][1]['topic'], "Economics")
        self.assertEqual(response_json['topics'][1]['clicked'], True)

        self.assertEqual(response_json['topics'][2]['topic'], "Environment")
        self.assertEqual(response_json['topics'][2]['clicked'], True)

        # Removing topics to user_1 preferences
        response = self.tester.post('http://localhost:5000/settings/topics', data = json.dumps(self.removing_topics_consumer), 
        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = json.loads(response.data)

        # Checking consumer_1 topics update
        self.assertEqual(response_json['status'], 'success')
        
        response = self.tester.get('http://localhost:5000/settings/topics', content_type='application/json',
        follow_redirects=True, headers=self.header)
        response_json = json.loads(response.data)
        
        # Changes didn't raise any exception
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['topics'][0]['topic'], "Cinema")
        self.assertEqual(response_json['topics'][0]['clicked'], True)

        self.assertEqual(response_json['topics'][2]['topic'], "Environment")
        self.assertEqual(response_json['topics'][2]['clicked'], True)

    def tearDown(self):
        # Retrieving consumers registered to test functionalities

        consumer_1 = Consumer.query.filter_by(username=self.consumer_1['username']).first()

        db.session.delete(consumer_1)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()
