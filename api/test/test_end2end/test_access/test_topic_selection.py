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
import sys
from api import app, db
import json

from models.consumer import *


class TestTopicSelection(unittest.TestCase):

    consumer_1 = {
          "name": "name_1",
          "surname": "last_name_1",
          "email": "test_front_email_topic@email.com",
          "username": "username_1",
          "password": "password_1",
    }

    tester = app.test_client()

    def setUp(self):
        self.desired_cap = []
        self.desired_cap.append({'browserName': 'chrome'})
        self.desired_cap.append({'browserName': 'firefox'})
        self.tester.post('http://localhost:5000/register', data = json.dumps(self.consumer_1), content_type='application/json', follow_redirects=True)
        cons = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        cons.email_checked = True
        db.session.add(cons)
        db.session.commit()

    def test_topic_selection(self):
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
                time.sleep(3)  
                element = self.driver.find_element(By.CSS_SELECTOR, ".btn")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()        
                self.driver.execute_script("window.scrollTo(0,0)")
                time.sleep(3)  
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, ".mb-0").click()
                self.driver.find_element(By.CSS_SELECTOR, ".mb-0").click()
                self.driver.find_element(By.CSS_SELECTOR, ".mb-0").click()
                self.driver.find_element(By.CSS_SELECTOR, ".stackable").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".mb-0").text
                self.assertEqual(text, "Topics Selection")
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(5) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(5) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, ".btn-danger").click()
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(9) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(10) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(11) .btn").click()
                self.driver.find_element(By.CSS_SELECTOR, ".btn-warning").click()
                self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
                self.driver.execute_script("window.scrollTo(0,0)")
                time.sleep(3)  
                self.driver.find_element(By.CSS_SELECTOR, ".medium").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".medium").text
                self.assertEqual(text, "Recommended News")
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()

    def tearDown(self):
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()

        if cons_1:
            db.session.delete(cons_1)

        db.session.commit()
        self.driver.quit()