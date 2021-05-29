from flask import current_app
import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app, db
from app.models import *

home_page = "http://127.0.0.1:5000/"

class BasicsTestCase(unittest.TestCase):
    @classmethod
    def setUp(self):
        # 打开浏览器
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(6)
        self.driver.get(home_page)
        # 创建测试app
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
