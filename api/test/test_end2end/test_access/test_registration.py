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
from api import app, db
import json
import sys

from models.consumer import *

class TestRegistrationStory(unittest.TestCase):

    consumer_1 = {
          "name": "name_1",
          "surname": "last_name_1",
          "email": "test_frontemail_1n@email.com",
          "username": "username_1",
          "password": "password_1",
    }

    consumer_2 = {
          "name": "name_2",
          "surname": "last_name_2",
          "email": "test_front_email_2@email.com",
          "username": "username_1",
          "password": "password_2",
    }

    consumer_3 = {
          "name": "name_3",
          "surname": "last_name_3",
          "email": "test_frontemail_1n@email.com",
          "username": "username_3",
          "password": "password_3",
    }

    tester = app.test_client()

    def setUp(self):
        self.desired_cap = []
        self.desired_cap.append({'browserName': 'chrome'})
        self.desired_cap.append({'browserName': 'firefox'})

    def test_confirm_email(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
                self.tearDown()
            self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
            confirm_email_value = Consumer.query.filter_by(email=self.consumer_1['email']).first().email_token
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )
            try:
                self.driver.get(f"http://web:8080/emailCheck/{confirm_email_value}")
                time.sleep(3)
                text = self.driver.find_element(By.ID, "message").text
                self.assertEqual(text, 'Your email address has been confirmed, now you can login inside PocketNews Network!!')
                self.driver.find_element(By.ID, "message").click()
                self.driver.find_element(By.ID, "message").click()
                self.driver.find_element(By.ID, "message").click()
                self.driver.find_element(By.LINK_TEXT, "login").click()
                self.driver.find_element(By.ID, "email").click()
                self.driver.find_element(By.NAME, "password").click()
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()
    def test_correct_registration(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
                cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
                self.tearDown()
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )
            try: 
                self.driver.get("http://web:8080/registration")
                self.driver.find_element(By.NAME, "first_name").click()
                self.driver.find_element(By.NAME, "first_name").send_keys(self.consumer_1['name'])
                self.driver.find_element(By.NAME, "username").send_keys(self.consumer_1['username'])
                self.driver.find_element(By.ID, "password").send_keys(self.consumer_1['password'])
                self.driver.find_element(By.NAME, "last_name").send_keys(self.consumer_1['surname'])
                self.driver.find_element(By.ID, "email").send_keys(self.consumer_1['email'])
                self.driver.find_element(By.NAME, "conf_password").send_keys(self.consumer_1['password'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                element = self.driver.find_element(By.CSS_SELECTOR, ".btn")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                time.sleep(3)
                element = self.driver.find_elements(By.NAME, "resend_email")
                self.assertNotEqual(element, [])
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()

    def test_expired_confirm_email(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
                self.driver.quit()
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )
            try:
                self.driver.get(f"http://web:8080/emailCheck/abc123")
                text = self.driver.find_element(By.ID, "message").text
                self.assertEqual(text, 'You have used a old email send to a not current email address...')
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()

    def test_wrong_registration_same_username(self):
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
                self.driver.quit()
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )
            try:
                self.driver.get("http://web:8080/registration")
                self.driver.find_element(By.NAME, "first_name").click()
                self.driver.find_element(By.NAME, "first_name").send_keys(self.consumer_2['name'])
                self.driver.find_element(By.NAME, "username").send_keys(self.consumer_2['username'])
                self.driver.find_element(By.ID, "password").send_keys(self.consumer_2['password'])
                self.driver.find_element(By.NAME, "last_name").send_keys(self.consumer_2['surname'])
                self.driver.find_element(By.ID, "email").send_keys(self.consumer_2['email'])
                self.driver.find_element(By.NAME, "conf_password").send_keys(self.consumer_2['password'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                element = self.driver.find_element(By.CSS_SELECTOR, ".btn")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                time.sleep(3)
                alert_text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(alert_text, 'In the system it exists already a user with this username')
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail() 
    
    def test_wrong_registration_same_email(self):
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
                self.driver.quit()
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )
            try:
                self.driver.get("http://web:8080/registration")
                self.driver.find_element(By.NAME, "first_name").click()
                self.driver.find_element(By.NAME, "first_name").send_keys(self.consumer_3['name'])
                self.driver.find_element(By.NAME, "username").send_keys(self.consumer_3['username'])
                self.driver.find_element(By.ID, "password").send_keys(self.consumer_3['password'])
                self.driver.find_element(By.NAME, "last_name").send_keys(self.consumer_3['surname'])
                self.driver.find_element(By.ID, "email").send_keys(self.consumer_3['email'])
                self.driver.find_element(By.NAME, "conf_password").send_keys(self.consumer_3['password'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                element = self.driver.find_element(By.CSS_SELECTOR, ".btn")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                time.sleep(3)
                alert_text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(alert_text, 'In the system it exists already a user with this email')
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()

    def tearDown(self):
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        cons_2 = Consumer.query.filter_by(email=self.consumer_2['email']).first()
        
        if cons_1:
            db.session.delete(cons_1)
        if cons_2:
            db.session.delete(cons_2)

        db.session.commit()
        self.driver.quit()