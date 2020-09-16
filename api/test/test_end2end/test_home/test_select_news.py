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

class TestSingleNews(unittest.TestCase):
    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "test_front_1@gmail.com",
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

    def test_select_single_news(self):
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
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0,0)")
                self.driver.find_element(By.CSS_SELECTOR, ".event:nth-child(1) .extra").click()
                time.sleep(2)
                element = self.driver.find_element(By.CSS_SELECTOR, ".event:nth-child(1) .extra")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                text = self.driver.find_element(By.CSS_SELECTOR, ".medium").text
                self.assertEqual(text, "Similar news")
                self.driver.find_element(By.CSS_SELECTOR, ".medium").click()
                self.driver.find_element(By.CSS_SELECTOR, ".home").click()
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()


    def tearDown(self):
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()

        if cons_1:
            db.session.delete(cons_1)

        self.driver.quit()
        db.session.commit()

