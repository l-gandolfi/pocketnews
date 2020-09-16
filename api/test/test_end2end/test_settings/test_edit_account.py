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


class TestEditAccount(unittest.TestCase):
    consumer_1 = {
        "name": "name_1",
        "surname": "last_name_1",
        "email": "email_edit_account1@gmail.com",
        "username": "user1",
        "password": "password_1",
    }
    consumer_2 = {
        "name": "name_2",
        "surname": "last_name_2",
        "email": "email_edit_account2@gmail.com",
        "username": "user2",
        "password": "password_2",
    }
    consumer_3 = {
        "name": "name_3",
        "surname": "last_name_3",
        "email": "email_edit_account3@gmail.com",
        "username": "user3",
        "password": "password_3",
    }



    tester = app.test_client()

    def registration(self, consumer):
        self.tester.post('http://localhost:5000/register', data = json.dumps(consumer), content_type='application/json', follow_redirects=True)
        cons = Consumer.query.filter_by(email=consumer['email']).first()
        cons.email_checked = True
        db.session.add(cons)
        topic = Topic.query.filter_by(id=0).first()
        topic.subscribe.append(cons)
        db.session.add(cons)
        db.session.commit()

    def setUp(self):
        self.desired_cap = []
        self.desired_cap.append({'browserName': 'chrome'})
        self.desired_cap.append({'browserName': 'firefox'})

        self.registration(self.consumer_1)
        self.registration(self.consumer_2)
        self.registration(self.consumer_3)

    def test_correct_email_change(self):
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
                self.driver.find_element(By.ID, "form-email-input").click()
                self.driver.find_element(By.ID, "form-email-input").send_keys('new_email@gmail.com')
                self.driver.find_element(By.ID, "form-confirmemail-input").click()
                self.driver.find_element(By.ID, "form-confirmemail-input").send_keys('new_email@gmail.com')
                self.driver.find_element(By.CSS_SELECTOR, ".btn-info").click()
                time.sleep(3)
                self.driver.find_element(By.CSS_SELECTOR, ".item:nth-child(4)").click()
                time.sleep(3)
                self.driver.find_element(By.CSS_SELECTOR, ".col-md-6:nth-child(1)").click()
                self.driver.find_element(By.ID, "email").click()
                self.driver.find_element(By.ID, "email").send_keys('new_email@gmail.com')
                self.driver.find_element(By.NAME, "password").click()
                self.driver.find_element(By.NAME, "password").send_keys(self.consumer_1['password'])
                self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
                time.sleep(3)
                self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1)").click()
                time.sleep(2)
                self.driver.find_element(By.CSS_SELECTOR, "v-flex").click()
                text = self.driver.find_element(By.CSS_SELECTOR, "h2").text 
                self.assertEqual(text, "A email has been sent to your email address, if you can't see it check spam box!")
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()

    def test_correct_edit_account(self):
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
                self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
                time.sleep(4)
                self.driver.find_element(By.CSS_SELECTOR, ".item:nth-child(3)").click()
                self.driver.find_element(By.CSS_SELECTOR, ".dividing").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".dividing").text
                self.assertEqual(text, "Account settings")
                self.driver.find_element(By.CSS_SELECTOR, "h5").click()
                text = self.driver.find_element(By.CSS_SELECTOR, "h5").text
                self.assertEqual(text, "In this page you can change or update your basic information.")
                self.driver.find_element(By.ID, "form-confirmpassword-group__BV_label_").click()
                self.driver.find_element(By.ID, "form-confirmpassword-group__BV_label_").click()
                element = self.driver.find_element(By.ID, "form-confirmpassword-group__BV_label_")
                actions = ActionChains(self.driver)
                actions.double_click(element).perform()
                self.driver.find_element(By.ID, "form-firstname-input").click()
                self.driver.find_element(By.ID, "form-firstname-input").send_keys("Gianni")
                self.driver.find_element(By.ID, "form-lastname-input").click()
                self.driver.find_element(By.ID, "form-lastname-input").send_keys("Bismark")
                self.driver.find_element(By.ID, "form-username-input").click()
                self.driver.find_element(By.CSS_SELECTOR, ".btn-info").click()
                time.sleep(3)
                text = self.driver.find_element(By.ID, "form-confirmpassword-group__BV_label_").text
                self.assertEqual(text, "Confirm your Password:")
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(text, "Information Updated")
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()

    def test_wrong_email_change(self):
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
                time.sleep(3)
                self.driver.find_element(By.CSS_SELECTOR, ".setting").click()
                self.driver.find_element(By.ID, "form-email-input").click()
                self.driver.find_element(By.ID, "form-email-input").send_keys(self.consumer_2['email'])
                self.driver.find_element(By.ID, "form-confirmemail-input").click()
                self.driver.find_element(By.ID, "form-confirmemail-input").send_keys(self.consumer_2['email'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn-info").click()
                time.sleep(2)
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(text, "Error while updating information. Email already taken.")
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()


    def test_wrong_username_change(self):
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
                time.sleep(3)
                self.driver.find_element(By.CSS_SELECTOR, ".setting").click()
                self.driver.find_element(By.LINK_TEXT, "Profile settings").click()
                self.driver.find_element(By.LINK_TEXT, "Account settings").click()
                element = self.driver.find_element(By.LINK_TEXT, "Account settings")
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                self.driver.find_element(By.LINK_TEXT, "Profile settings").click()
                self.driver.find_element(By.LINK_TEXT, "Account settings").click()
                self.driver.find_element(By.ID, "form-username-input").click()
                self.driver.find_element(By.ID, "form-username-input").send_keys(self.consumer_2['username'])
                self.driver.find_element(By.CSS_SELECTOR, ".btn-info").click()
                time.sleep(2)
                self.driver.find_element(By.CSS_SELECTOR, ".alert").click()
                text = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
                self.assertEqual(text, "Error while updating information. Username already taken.")
            except:
                error = sys.exc_info()[0]
                print(error)
                self.fail()



    def tearDown(self):
        cons_1 = Consumer.query.filter_by(email=self.consumer_1['email']).first()
        cons_2 = Consumer.query.filter_by(email=self.consumer_2['email']).first()
        cons_3 = Consumer.query.filter_by(email=self.consumer_3['email']).first()

        if not(cons_1):
            cons_1 = Consumer.query.filter_by(email='new_email@gmail.com').first()

        db.session.delete(cons_1)
        db.session.delete(cons_2)
        db.session.delete(cons_3)

        self.driver.quit()
        db.session.commit()
