import re
import threading
import time
from flask import current_app
import unittest
from selenium import webdriver
from app import create_app, db
from app.models import *

class StudentTestCase(unittest.TestCase):
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

    def test_empty_username_password(self):
        """ 测试用户名与密码为空的情况[当参数不全的话，返回code=-2] """
        # 使用客户端向后端发送post请求, data指明发送的数据，会返回一个响应对象
        response = self.app.test_client().post('/login', data={})
        # respoonse.data是响应体数据
        json_data = response.data
        # 按照json解析
        json_dict = json.loads(json_data)
        # 使用断言进行验证：是否存在code字符串在字典中
        self.assertIn('code', json_dict, '数据格式返回错误')
        # 获取errcode的返回码的值，验证是否为错误码 -2
        code = json_dict.get("errcode")
        self.assertEqual(code, -2, '状态码返回错误')

    def test_error_username_password(self):
        """测试用户名和密码错误的情况[当登录名和密码错误的时候，返回 code = -1]"""
        response = self.app.test_client().post('/login', data={"username": "aaaaa", "password": "12343"})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('code', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['code'], -1, '状态码返回错误')

    def test_login_correct(self):
        """测试正确登录，跳转到homePage"""
        response = self.app.test_client().post('/login', data={"username": "123456", "password": "123456"})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('code', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['code'], 0, '状态码返回错误')

    def test_edit_correct(self):
        """测试正确编辑个人信息"""
        response = self.app.test_client().post('/login', data={"username": "123456", "password": "123456"})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('code', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['code'], 1, '状态码返回错误')

    def test_join_course_correct(self):
        """测试正确加入课程"""
        response = self.app.test_client().post('/login', data={"username": "123456", "password": "123456"})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('code', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['code'], 2, '状态码返回错误')

    def test_quit_course_correct(self):
        """测试正确退出课程"""
        response = self.app.test_client().post('/login', data={"username": "123456", "password": "123456"})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('code', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['code'], 3, '状态码返回错误')

    def test_check_in_correct(self):
        """测试正确签到"""
        response = self.app.test_client().post('/login', data={"username": "123456", "password": "123456"})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('code', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['code'], 4, '状态码返回错误')
