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
from selenium.webdriver.support.ui import WebDriverWait
import psycopg2
import unittest
import warnings
import ast
import sys
from api import app, db
import json
import datetime

from models.consumer import *
from models.topic import *

class TestResetPSW(unittest.TestCase):

    consumer_1 = {
          "user_id": '',
          "name": "name_1",
          "surname": "last_name_1",
          "email": "test_front_email1@email.com",
          "username": "username_1",
          "password": "password_1",
    }

    consumer_2 = {
          "user_id": '',
          "name": "name_2",
          "surname": "last_name_2",
          "email": "test_front_email2@email.com",
          "username": "username_2",
          "password": "password_2",
    }

    payload_request = {
        'email': consumer_1['email'],
        'op_id': 0,
    }

    payload_request_2 = {
        'email': consumer_2['email'],
        'op_id': 0,
    }


    payload_send_new_password = {
        'user_id': '',
        'password': 'new_password',
        'op_id': 1,
    }

    tester = app.test_client()

    def setUp(self):
        self.desired_cap = []
        self.desired_cap.append({'browserName': 'chrome'})
        self.desired_cap.append({'browserName': 'firefox'})
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
        self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_request), content_type='application/json', follow_redirects=True)
        consumer = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        self.consumer_1['user_id'] = consumer.id
        new_reset_psw_data = consumer.reset_psw_date - datetime.timedelta(seconds=200)
        consumer.reset_psw_date = new_reset_psw_data
        db.session.add(consumer)
        db.session.commit()

        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), content_type='application/json', follow_redirects=True)
        consumer = Consumer.query.filter_by(email=self.consumer_2['email']).first()
        self.consumer_2['user_id'] = consumer.id
        consumer.email_checked = True
        topic = Topic.query.filter_by(id=0).first()
        topic.subscribe.append(consumer)
        db.session.add(consumer)
        db.session.commit()
        self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_request_2), content_type='application/json', follow_redirects=True)

    def test_correct_request(self):
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
                self.driver.find_element(By.LINK_TEXT, "Forgot the password?").click()
                self.driver.find_element(By.ID, "email").click()
                self.driver.find_element(By.ID, "email").send_keys(self.consumer_1['email'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                time.sleep(3)  
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text 
                username = self.consumer_1['username']
                self.assertEqual(text, f'Hi {username}! A email with password reset instructions has been sent to your email adress!')
            except:
                error = sys.exc_info()[0]
                if error == "<class 'selenium.common.exceptions.WebDriverException'>":
                    print(error)
                    self.fail()

    def test_correct_reset(self):
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
                self.tearDown()
                self.setUp()
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )

            try:
                self.driver.get(f"http://web:8080/changePassword/{self.consumer_2['user_id']}")
                time.sleep(3)  
                self.driver.find_element(By.ID, "password").click()
                self.driver.find_element(By.ID, "password").send_keys("ABC123")
                self.driver.find_element(By.NAME, "conf_password").click()
                self.driver.find_element(By.NAME, "conf_password").send_keys("ABC123")
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

                WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')
                alert = self.driver.switch_to.alert
                alert.accept()
                time.sleep(2) 
                element = self.driver.find_element(By.NAME, "email")
                self.assertNotEqual(element, [])
                self.driver.find_element(By.NAME, "email").send_keys(self.consumer_2['email'])
                self.driver.find_element(By.NAME, "password").send_keys('ABC123')
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                element = self.driver.find_element(By.CSS_SELECTOR, ".btn")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                time.sleep(2)
                self.driver.find_element(By.CSS_SELECTOR, ".medium").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".medium").text
                self.assertEqual(text, "Recommended News")
            except:
                error = sys.exc_info()[0]
                if error == "<class 'selenium.common.exceptions.WebDriverException'>":
                    print(error)
                    self.fail()

    def test_wrong_reset_password_request(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
                self.tearDown()
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )
            try:
                self.driver.get("http://web:8080/login")
                self.driver.find_element(By.ID, "email").click()
                self.driver.find_element(By.LINK_TEXT, "Forgot the password?").click()
                self.driver.find_element(By.ID, "email").click()
                self.driver.find_element(By.ID, "email").send_keys('no@email.com')
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                time.sleep(2)
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                element = self.driver.find_element(By.CSS_SELECTOR, ".alert")
                actions = ActionChains(self.driver)
                actions.double_click(element).perform()
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3)").click()
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(text, "No one account is recorded with this email. Are you sure about your pocketNews subscription?")
            except:
                error = sys.exc_info()[0]
                if error == "<class 'selenium.common.exceptions.WebDriverException'>":
                    print(error)
                    self.fail()

    def test_reset_psw_expired_time(self):
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
                self.driver.get(f"http://web:8080/changePassword/{self.consumer_1['user_id']}")
                WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')
                alert = self.driver.switch_to.alert
                text = alert.text
                self.assertEqual(text, 'The request is expired! Get another one!')
                alert.accept()
                time.sleep(2)  
                text = self.driver.find_element(By.CSS_SELECTOR, "h2").text
                self.assertEqual(text, "Insert the email address that you use to access into PocketNews")
            except:
                error = sys.exc_info()[0]
                if error == "<class 'selenium.common.exceptions.WebDriverException'>":
                    print(error)
                    self.fail()

    def test_multiple_request(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
                self.tearDown()
                self.setUp()
            self.payload_send_new_password['user_id'] = self.consumer_1['user_id']
            self.tester.post('http://localhost:5000/reset_psw', data = json.dumps(self.payload_send_new_password), content_type='application/json', follow_redirects=True)
            self.driver = webdriver.Remote(
                command_executor='http://selenium-hub:4444/wd/hub',
                desired_capabilities=cap,
            )
            try:
                self.driver.get(f"http://web:8080/changePassword/{self.consumer_1['user_id']}")
                WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')
                alert = self.driver.switch_to.alert
                text = alert.text
                self.assertEqual(text, 'The request is expired! Get another one!')
                alert.accept()
                time.sleep(2)  
                text = self.driver.find_element(By.CSS_SELECTOR, "h2").text
                self.assertEqual(text, "Insert the email address that you use to access into PocketNews")
            except:
                error = sys.exc_info()[0]
                if error == "<class 'selenium.common.exceptions.WebDriverException'>":
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

