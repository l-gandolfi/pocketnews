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

class TestLikeNews(unittest.TestCase):

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
        'topic': 'politics',
        'id': 0
        },
        {
        'topic': 'news',
        'id': 1
        }
    ],
    "user_id": ""
    }

    news_like_1= {
    "news_id": 500
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
      
    def test_like_news(self):
        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)
        response_json = json.loads(response.data.decode('utf-8'))

        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }

        self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer), 
        content_type='application/json', follow_redirects=True, headers=self.header)
        # Like a news
        response = self.tester.post('http://localhost:5000/social/like', data = json.dumps(self.news_like_1),
        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['status'], 'success')

        # Get users that liked this news and check if consumer_1 belongs to returned array
        response = self.tester.post('http://localhost:5000/social/favorite', data = json.dumps(self.news_like_1),
        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = json.loads(response.data)
        self.assertEqual(len(response_json['users']), 1)
        consumer_id =  Consumer.query.filter_by(email=self.consumer_1['email']).first().id
        self.assertIn(consumer_id, response_json['users'])

        # Disike previously liked news
        response = self.tester.post('http://localhost:5000/social/dislike', data = json.dumps(self.news_like_1),
        content_type='application/json', follow_redirects=True, headers=self.header)
        self.assertEqual(response_json['status'], 'success')

        # Get users that liked this news and check if consumer_1 do not belongs to returned array
        response = self.tester.post('http://localhost:5000/social/favorite', data = json.dumps(self.news_like_1),
        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = json.loads(response.data)
        self.assertEqual(len(response_json['users']), 0)
        consumer_id =  Consumer.query.filter_by(email=self.consumer_1['email']).first().id
        self.assertNotIn(consumer_id, response_json['users'])


    def tearDown(self):
        # Retrieving consumers registered to test functionalities

        consumer_1 = Consumer.query.filter_by(username=self.consumer_1['username']).first()

        db.session.delete(consumer_1)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()
