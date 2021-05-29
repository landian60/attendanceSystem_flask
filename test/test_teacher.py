import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app, db
from app.models import *


class TeacherTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        try:
            cls.client = webdriver.Chrome(chrome_options=options)
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # create the database and populate with some fake data
            db.create_all()

            # add a teacher
            u = User(uuid='120170317', password='123456', user_type='teacher')
            db.session.add(u)
            db.session.commit()
            t = TeacherInfo(('20170317', 'teacher_test', '18262626666', '123@hhu.edu.cn', '120170317'))
            db.session.add(t)
            db.session.commit()

            # start the Flask server in a thread
            cls.server_thread = threading.Thread(target=cls.app.run,
                                                 kwargs={'debug': False})
            cls.server_thread.start()

            # give the server a second to ensure it is up
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop the flask server and the browser
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.quit()
            cls.server_thread.join()

            # destroy database
            db.drop_all()
            db.session.remove()

            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_my(self):
        # navigate to home page
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('欢迎来到考勤系统！', self.client.page_source))

        # navigate to login page
        self.client.find_element_by_link_text('登录').click()
        self.assertIn('<h1>登录</h1>', self.client.page_source)

        # login
        self.client.find_element_by_name('user_type').send_keys('教师')
        self.client.find_element_by_name('user_id').send_keys('20170317')
        self.client.find_element_by_name('password').send_keys('123456')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('工号：20170317', self.client.page_source))
