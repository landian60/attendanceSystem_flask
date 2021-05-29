import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import *


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_verify_password(self):
        u = User()
        u.password = '123456'
        self.assertTrue(u.verify_password('123456'))
        self.assertFalse(u.verify_password('12345'))

    def test_init_StudentInfo(self):
        s = StudentInfo(('1606010310', 'dexter', '18262626666', '123456@hhu.edu.cn', '01606010310'))
        self.assertTrue(s.stu_id == '1606010310')
        self.assertTrue(s.stu_name == 'dexter')
        self.assertTrue(s.phone_number == '18262626666')
        self.assertTrue(s.email == '123456@hhu.edu.cn')
        self.assertTrue(s.uuid == '01606010310')

    def test_init_TeacherInfo(self):
        t = TeacherInfo(('20170317', 'hi', '18262626666', '123456@hhu.edu.cn', '120170317'))
        self.assertTrue(t.teacher_id == '20170317')
        self.assertTrue(t.teacher_name == 'hi')
        self.assertTrue(t.phone_number == '18262626666')
        self.assertTrue(t.email == '123456@hhu.edu.cn')
        self.assertTrue(t.uuid == '120170317')

    def test_init_CourseInfo(self):
        c = CourseInfo(('53241', 'database_test', 'welcome', '120170317'))
        self.assertTrue(c.course_id == '53241')
        self.assertTrue(c.course_name == 'database_test')
        self.assertTrue(c.course_intro == 'welcome')
        self.assertTrue(c.teacher_id == '120170317')
