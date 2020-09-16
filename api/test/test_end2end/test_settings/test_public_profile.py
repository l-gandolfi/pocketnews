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

class TestPublicProfile(unittest.TestCase):
    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "test_front_modpub@gmail.com",
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

    def test_modify_public_profile(self):
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
                self.driver.find_element(By.ID, "email").click()
                element = self.driver.find_element(By.ID, "email")
                actions = ActionChains(self.driver)
                actions.double_click(element).perform()
                self.driver.find_element(By.ID, "email").click()
                self.driver.find_element(By.ID, "email").send_keys(self.consumer_1['email'])
                self.driver.find_element(By.NAME, "password").click()
                self.driver.find_element(By.NAME, "password").send_keys(self.consumer_1['password'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                time.sleep(2)
                self.driver.find_element(By.CSS_SELECTOR, ".item:nth-child(3)").click()
                self.driver.find_element(By.LINK_TEXT, "Profile settings").click()
                self.driver.find_element(By.ID, "form-city-group").click()
                self.driver.find_element(By.CSS_SELECTOR, "#form-city-group .custom-control-label").click()
                self.driver.find_element(By.ID, "form-city-input").click()
                self.driver.find_element(By.ID, "form-city-input").send_keys("Milano")
                self.driver.find_element(By.CSS_SELECTOR, "#form-topics-group .custom-control-label").click()
                self.driver.find_element(By.CSS_SELECTOR, ".dividing").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".dividing").text
                self.assertEqual(text, "Profile settings")
                self.driver.find_element(By.CSS_SELECTOR, "h5").click()
                text = self.driver.find_element(By.CSS_SELECTOR, "h5").text
                self.assertEqual(text, "In this page you can change or update your public profile information.")
                self.driver.find_element(By.CSS_SELECTOR, ".btn-info").click()
                self.driver.find_element(By.CSS_SELECTOR, ".four > .item:nth-child(2)").click()
                time.sleep(2)
                self.driver.find_element(By.CSS_SELECTOR, ".col-md-6:nth-child(2) > h6").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".col-md-6:nth-child(2) > h6").text
                self.assertEqual(text, "Favourite topics")
                self.driver.find_element(By.CSS_SELECTOR, ".col-md-6 > div").click()
                self.driver.find_element(By.CSS_SELECTOR, ".setting").click()
                self.driver.find_element(By.LINK_TEXT, "Profile settings").click()
                self.driver.find_element(By.CSS_SELECTOR, "#form-city-group > .bv-no-focus-ring").click()
                self.driver.find_element(By.CSS_SELECTOR, "#form-city-group .custom-control-label").click()
                self.driver.find_element(By.CSS_SELECTOR, "#form-topics-group .custom-control-label").click()
                self.driver.find_element(By.CSS_SELECTOR, ".form").click()
                self.driver.find_element(By.CSS_SELECTOR, ".btn-info").click()
                time.sleep(3)
                element = self.driver.find_element(By.CSS_SELECTOR, ".btn-info")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                element = self.driver.find_element(By.CSS_SELECTOR, "body")
                actions = ActionChains(self.driver)
                self.driver.find_element(By.CSS_SELECTOR, ".four > .item:nth-child(2)").click()
                self.driver.find_element(By.CSS_SELECTOR, ".item:nth-child(4)").click()

            except:
                error = sys.exc_info()[0]
                if error == "<class 'selenium.common.exceptions.WebDriverException'>":
                    print(error)
                    self.fail()

    def test_visualize_public_profile(self):
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
                self.driver.find_element(By.CSS_SELECTOR, ".ui > .item:nth-child(2)").click()
                self.driver.find_element(By.CSS_SELECTOR, ".mb-3").click()
                self.driver.find_element(By.CSS_SELECTOR, ".mb-3").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".mb-3").text
                self.assertEqual(text, self.consumer_1['username'])
                self.driver.find_element(By.CSS_SELECTOR, ".mt-2:nth-child(2)").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".mt-2:nth-child(2)").text
                self.assertEqual(text, f'{self.consumer_1["name"]} {self.consumer_1["surname"]}')
                self.driver.find_element(By.CSS_SELECTOR, ".my-2").click()
                self.driver.find_element(By.CSS_SELECTOR, ".mt-2:nth-child(3)").click()
                self.driver.find_element(By.CSS_SELECTOR, ".my-2").click()
                self.driver.find_element(By.CSS_SELECTOR, ".mt-2:nth-child(3)").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".mt-2:nth-child(3)").text
                self.driver.find_element(By.CSS_SELECTOR, ".item:nth-child(4)").click()
                self.assertEqual(text, self.consumer_1['email'])
            except:
                error = sys.exc_info()[0]
                if error == "<class 'selenium.common.exceptions.WebDriverException'>":
                    print(error)
                    self.fail()


    def tearDown(self):
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()

        if cons_1:
            db.session.delete(cons_1)

        self.driver.quit()
        db.session.commit()

