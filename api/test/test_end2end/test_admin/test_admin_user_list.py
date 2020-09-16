import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import unittest
import warnings
import ast
from api import app, db
import json
import sys

from models.consumer import *
from models.topic import *

class TestAdminUserList(unittest.TestCase):
    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "test_front_list1@gmail.com",
        "username": "user1",
        "password": "password_1",
    }
    consumer_2 = {
        "name": "name_2",
        "surname": "last_name_2",
        "email": "test_front_list_2@gmail.com",
        "username": "user2",
        "password": "password_2",
    }
    consumer_3 = {
        "name": "name_3",
        "surname": "last_name_3",
        "email": "test_front_list_3@gmail.com",
        "username": "user3",
        "password": "password_3",
    }

    tester = app.test_client()

    def setUp(self):
        self.desired_cap = []
        self.desired_cap.append({'browserName': 'chrome'})
        self.desired_cap.append({'browserName': 'firefox'})
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), content_type='application/json', follow_redirects=True)
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_3), content_type='application/json', follow_redirects=True)

        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        cons_1.email_checked = True
        db.session.add(cons_1)
        topic = Topic.query.filter_by(id=0).first()
        topic.subscribe.append(cons_1)
        db.session.add(cons_1)
        db.session.commit()
    
    def test_user_list(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
                self.tearDown()
                self.setUp()
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )
            try:
                self.driver.get("http://web:8080/login")
                self.driver.find_element(By.NAME, "email").click()
                self.driver.find_element(By.NAME, "email").click()
                element = self.driver.find_element(By.NAME, "email")
                actions = ActionChains(self.driver)
                actions.double_click(element).perform()
                self.driver.find_element(By.NAME, "email").click()
                self.driver.find_element(By.NAME, "email").send_keys(self.consumer_1['email'])
                self.driver.find_element(By.NAME, "password").click()
                self.driver.find_element(By.NAME, "password").send_keys(self.consumer_1['password'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                element = self.driver.find_element(By.CSS_SELECTOR, ".btn")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                time.sleep(3)
                self.driver.get("http://web:8080/admin/users")
                self.driver.set_window_size(926, 697)
                self.driver.find_element(By.CSS_SELECTOR, ".stackable").click()
                self.driver.find_element(By.CSS_SELECTOR, ".stackable").click()
                self.driver.find_element(By.CSS_SELECTOR, ".card-title").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".card-title").text
                self.assertEqual(text, "Administrator Panel: Users List") 
                text = self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .btn").text
                self.assertIn(text, ['user1', 'user2', 'user3'])
                text = self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) .btn").text
                self.assertIn(text, ['user1', 'user2', 'user3'])
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) .btn").click()
                element = self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) .btn")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                element = self.driver.find_element(By.CSS_SELECTOR, "body")
                actions = ActionChains(self.driver)
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1)").click()
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()
    
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
        