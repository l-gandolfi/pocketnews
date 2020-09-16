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

class TestLogin(unittest.TestCase):

    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "test_front_email_login@gmail.com",
        "username": "user1",
        "password": "password_1",
    }

    consumer_2 = {
        "name": "name_2",
        "surname": "last_name_2",
        "email": "test_front_email_2_login@gmail.com",
        "username": "user2",
        "password": "password_2",
    }

    consumer_3 = {
        "name": "name_3",
        "surname": "last_name_3",
        "email": "test_front_email_3_login@gmail.com",
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
        cons_2 = Consumer.query.filter_by(email=self.consumer_2['email']).first()
        cons_2.email_checked = True
        db.session.add(cons_2)
        db.session.commit()
        topic = Topic.query.filter_by(id=0).first()
        topic.subscribe.append(cons_2)
        db.session.add(cons_2)
        db.session.commit()

        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_3), content_type='application/json', follow_redirects=True)
        cons_3 = Consumer.query.filter_by(email=self.consumer_3['email']).first()
        cons_3.email_checked = True
        db.session.add(cons_3)
        db.session.commit()

    def test_correct_login_no_conf_email(self):
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
                element = self.driver.find_elements(By.NAME, "no-element-in-page")
                self.assertEqual(element, [])
                element = self.driver.find_elements(By.NAME, "resend_email")
                self.assertNotEqual(element, [])
            except:
                error = sys.exc_info()[0]
                if not(error == "<class 'selenium.common.exceptions.WebDriverException'>"):
                    print(error)
                    self.fail()

    def test_correct_login_no_topic(self):
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
                self.driver.find_element(By.NAME, "email").send_keys(self.consumer_3['email'])
                self.driver.find_element(By.NAME, "password").click()
                self.driver.find_element(By.NAME, "password").send_keys(self.consumer_3['password'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                element = self.driver.find_element(By.CSS_SELECTOR, ".btn")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                time.sleep(3)            
                text = self.driver.find_element(By.CSS_SELECTOR, ".mb-0").text
                self.assertEqual(text, "Topics Selection")
            except:
                error = sys.exc_info()[0]
                if not(error == "<class 'selenium.common.exceptions.WebDriverException'>"):
                    print(error)
                    self.fail()

    def test_wrong_login(self):
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
                self.driver.find_element(By.NAME, "email").send_keys("g@gmail.com")
                self.driver.find_element(By.NAME, "password").click()
                self.driver.find_element(By.NAME, "password").send_keys("abc123")
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                element = self.driver.find_element(By.CSS_SELECTOR, ".btn")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                alert_text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(alert_text, 'Wrong email or password')
            except:
                error = sys.exc_info()[0]
                if not(error == "<class 'selenium.common.exceptions.WebDriverException'>"):
                    print(error)
                    self.fail()

    def test_correct_login(self):
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
                self.driver.find_element(By.NAME, "email").send_keys(self.consumer_2['email'])
                self.driver.find_element(By.NAME, "password").click()
                self.driver.find_element(By.NAME, "password").send_keys(self.consumer_2['password'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                element = self.driver.find_element(By.CSS_SELECTOR, ".btn")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()        
                self.driver.execute_script("window.scrollTo(0,0)")
                time.sleep(3)    
                self.driver.find_element(By.CSS_SELECTOR, ".medium").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".medium").text
                self.assertEqual(text, "Recommended News")
            except:
                error = sys.exc_info()[0]
                if not(error == "<class 'selenium.common.exceptions.WebDriverException'>"):
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

        db.session.commit()
        self.driver.quit()