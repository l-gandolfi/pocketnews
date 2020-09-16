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
from selenium.webdriver.support.wait import WebDriverWait


class TestDeleteAccount(unittest.TestCase):
    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "test_front_delete@gmail.com",
        "username": "user1",
        "password": "password_1",
    }
    tester = app.test_client()

    def setUp(self):
        self.desired_cap = []
        self.desired_cap.append({'browserName': 'chrome'})
        self.desired_cap.append({'browserName': 'firefox'})
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)

        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        cons_1.email_checked = True
        db.session.add(cons_1)
        topic = Topic.query.filter_by(id=0).first()
        topic.subscribe.append(cons_1)
        db.session.add(cons_1)
        db.session.commit()

    def test_delete_account(self):
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
                self.driver.find_element(By.ID, "email").click()
                self.driver.find_element(By.ID, "email").send_keys(self.consumer_1['email'])
                self.driver.find_element(By.NAME, "password").click()
                self.driver.find_element(By.NAME, "password").send_keys(self.consumer_1['password'])
                self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
                time.sleep(4)
                self.driver.find_element(By.CSS_SELECTOR, ".setting").click()
                time.sleep(5)
                self.driver.find_element(By.CSS_SELECTOR, ".btn-outline-danger").click()
                self.driver.find_element(By.CSS_SELECTOR, ".btn-danger").click()
                time.sleep(2)
                self.driver.find_element(By.ID, "email").click()
                self.driver.find_element(By.ID, "email").send_keys(self.consumer_1['email'])
                self.driver.find_element(By.NAME, "password").click()
                self.driver.find_element(By.NAME, "password").send_keys(self.consumer_1['password'])
                self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
                time.sleep(2)
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(text, "Wrong email or password")  
            except:
                error = sys.exc_info()[0]
                if not(error == "<class 'selenium.common.exceptions.TimeoutException'>"):
                    print(error)
                    self.fail()

    def tearDown(self):
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()

        if cons_1:
            db.session.delete(cons_1)

        self.driver.quit()
        db.session.commit()
