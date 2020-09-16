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
import sys
from api import app, db
import json

from models.consumer import *

class TestResendEmail(unittest.TestCase):

    consumer_1 = {
          "name": "name_1",
          "surname": "last_name_1",
          "email": "test_front_email_1@email.com",
          "username": "username_1",
          "password": "password_1",
    }

    consumer_2 = {
        "name": "name_2",
        "surname": "last_name_2",
        "email": "test_front_email_2@gmail.com",
        "username": "user2",
        "password": "password_2",
        "email_checked": '',
    }

    tester = app.test_client()

    def setUp(self):
        self.desired_cap = []
        self.desired_cap.append({'browserName': 'chrome'})
        self.desired_cap.append({'browserName': 'firefox'})

    def test_already_used_email(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
                self.tearDown()
            self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_2), content_type='application/json', follow_redirects=True)
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
                self.driver.find_element(By.NAME, "resend_email").send_keys(self.consumer_2['email'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                time.sleep(3)
                alert_text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(alert_text, 'Email already used!')
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()

    def test_resend_email(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
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
                self.driver.find_element(By.NAME, "resend_email").send_keys(self.consumer_1['email'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                time.sleep(3)
                alert_text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(alert_text, 'A new email has been sent')
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()

    def test_block_resend_email(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        for cap in self.desired_cap:
            if cap['browserName'] == 'firefox':
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
                consumer = Consumer.query.filter_by(email=self.consumer_1['email']).first()
                consumer.email_checked = True
                db.session.add(consumer)
                db.session.commit()
                self.driver.find_element(By.NAME, "resend_email").send_keys(self.consumer_1['email'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                time.sleep(3)
                alert_text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(alert_text, 'Email already checked!')
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
