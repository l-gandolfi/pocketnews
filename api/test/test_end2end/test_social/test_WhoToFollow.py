import ast
import json
import os
import sys
import time
import unittest
import warnings

import psycopg2
from api import app, db
from models.consumer import *
from models.topic import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait


class TestWhoToFollow(unittest.TestCase):
    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "email1@mail.it",
        "username": "user1",
        "password": "password_1",
    }
    consumer_2 = {
        "name": "name_2",
        "surname": "last_name_2",
        "email": "email2@mail.it",
        "username": "user2",
        "password": "password_2",
    }
    consumer_3 = {
        "name": "name_3",
        "surname": "last_name_3",
        "email": "email3@mail.it",
        "username": "user3",
        "password": "password_3",
    }
    
    tester = app.test_client()


    def setUp(self):
        self.desired_cap = []
        #self.desired_cap.append({'browserName': 'chrome'})
        self.desired_cap.append({'browserName': 'firefox'})
        
        # Consumer 1: topics = 0, 1
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)

        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        cons_1.email_checked = True
        db.session.add(cons_1)
        topic = Topic.query.filter_by(id=7).first()
        topic.subscribe.append(cons_1)
        topic = Topic.query.filter_by(id=8).first()
        topic.subscribe.append(cons_1)
        db.session.add(cons_1)
        db.session.commit()
        
        # Consumer 2: topics = 0, 2
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), content_type='application/json', follow_redirects=True)

        cons_2 = Consumer.query.filter_by(email=self.consumer_2['email']).first()
        cons_2.email_checked = True
        db.session.add(cons_2)
        topic = Topic.query.filter_by(id=6).first()
        topic.subscribe.append(cons_2)
        topic = Topic.query.filter_by(id=8).first()
        topic.subscribe.append(cons_2)
        db.session.add(cons_2)
        db.session.commit()
        
        # Consumer 3: topics = 1
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_3), content_type='application/json', follow_redirects=True)

        cons_3 = Consumer.query.filter_by(email=self.consumer_3['email']).first()
        cons_3.email_checked = True
        db.session.add(cons_3)
        topic = Topic.query.filter_by(id=8).first()
        topic.subscribe.append(cons_3)
        db.session.add(cons_3)
        db.session.commit()



    def tearDown(self):
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        cons_2 = Consumer.query.filter_by(email=self.consumer_2['email']).first()
        cons_3 = Consumer.query.filter_by(email=self.consumer_3['email']).first()

        if cons_1:
            db.session.delete(cons_1)
        if cons_2:
            db.session.delete(cons_2)
        if cons_3:
            db.session.delete(cons_3)

        self.driver.quit()
        db.session.commit()
  
    def test_who_to_follow(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )
            try:
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
                suggest_menu = wait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.ID, "follow_him"))
                    )
                follow_text = suggest_menu.text
                
                self.assertEqual(follow_text,"Follow")
                
                self.driver.find_element(By.ID, "refresh").click()
                suggest_menu = wait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "follow_him"))
                    )
          
                # START THIS FOLLOWINGGGGG
                self.driver.find_element(By.ID, "follow_him").click()
                time.sleep(1)
                self.driver.find_element(By.ID, "follow_him").click()                
                time.sleep(1)
                
                self.driver.find_element_by_id("profile_button").click()
                
                following = wait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "following")))
                following_text = following.text
                self.assertEqual(following_text, 'Following\n2')
                
                self.driver.find_element_by_id("following").click()
                time.sleep(1)
                self.driver.find_element(By.ID, "home_button").click()
                
    
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()

if __name__ == '__main__':
    unittest.main()     
