import ast
import json
import os
import time
import unittest
import warnings

import psycopg2
from api import app, db
from flask_bcrypt import check_password_hash, generate_password_hash
from models import *
from models.consumer import *
from models.interested_in import *
from models.like import *
from models.news import *
from models.recommended import *
from models.topic import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import desc


class TestTopicSettings(unittest.TestCase):
    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "email_login@gmail.com",
        "username": "user1",
        "password": "password_1",
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

    tester = app.test_client()

    def setUp(self):
        self.desired_cap = []
        # self.desired_cap.append({'browserName': 'chrome'})
        self.desired_cap.append({'browserName': 'firefox'})
  
    def test_correct_topic_visualization(self):

        # Performing user registration
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        response =  self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), 
        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))
        consumer_id =  Consumer.query.filter_by(email=self.consumer_1['email']).first().id
        self.topics_consumer['user_id'] = consumer_id

        consumer =  Consumer.query.filter_by(email=self.consumer_1['email']).first()
        consumer.email_checked = True
        db.session.commit()

        response = self.tester.post('http://localhost:5000/login', data = json.dumps(self.consumer_1), 
                                        content_type='application/json', follow_redirects=True)
        response_json = ast.literal_eval(response.data.decode('utf-8'))

        self.header = {
            'Authorization': 'Bearer {}'.format(response_json["data"]["access_token"])
        }
        response = self.tester.post('http://localhost:5000/topics', data = json.dumps(self.topics_consumer), 
        content_type='application/json', follow_redirects=True, headers=self.header)
        response_json = ast.literal_eval(response.data.decode('utf-8'))

        response = self.tester.get('http://localhost:5000/settings/topics', content_type='application/json', 
        follow_redirects=True, headers=self.header)
        response_json = json.loads(response.data)

        # From this point e2e test will start
        for cap in self.desired_cap:
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )
            # Logging into PocketNews webapp
            self.driver.get("http://web:8080/login")
            self.driver.find_element(By.NAME, "email").click()
            self.driver.find_element(By.NAME, "email").send_keys(self.consumer_1["email"])
            self.driver.find_element(By.NAME, "password").click()
            self.driver.find_element(By.NAME, "password").send_keys(self.consumer_1["password"])
            element = self.driver.find_element(By.CSS_SELECTOR, ".btn")
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
            time.sleep(2)
            
            # Navigation to settings section
            self.driver.find_element_by_id("settings_button").click()

            # Navigation to topic settings
            self.driver.find_element(By.LINK_TEXT, "Topic settings").click()
            element = self.driver.find_element(By.LINK_TEXT, "Topic settings")
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            element = self.driver.find_element(By.CSS_SELECTOR, "body")       
            time.sleep(2)

            # Trying to perform an invalid operation (no topic selected)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
        
            # Clearing all topics already selected
            self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .ui").click()
            self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) .ui").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn-info").click()
            
            # At this point submit will be blocked and previously selected topics restored
            # An error messagge inside an alert will be diplayed
            # Assert alert text value for invalid opeartion 
            assert self.driver.find_element(By.CSS_SELECTOR, ".alert").text == "Error while updating preferences. You must select at least one topic"

            # Trying to perform a valid operation (select one more topic)
            self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) .ui").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn-info").click()
            assert self.driver.find_element(By.CSS_SELECTOR, ".alert").text == "Information Updated"

    def tearDown(self):
        # Deleting signed up user
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()

        if cons_1:
            db.session.delete(cons_1)

        db.session.commit()
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
