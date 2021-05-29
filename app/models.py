from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    uuid = db.Column(db.String(11), primary_key=True)
    password = db.Column(db.String(15), nullable=False)
    user_type = db.Column(db.Enum('student', 'teacher', 'admin'), nullable=False)

    def get_id(self):
        return self.uuid

    def verify_password(self, password):
        return self.password == password

    def __repr__(self):
        return self.uuid

    @property
    def serialize(self):
        return {
            'uuid': self.uuid,
            'password': self.password,
            'user_type': self.user_type,
        }


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class StudentInfo(db.Model):
    __tablename__ = 'student_info'

    stu_id = db.Column(db.String(10), primary_key=True)
    stu_name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(11))
    email = db.Column(db.String(30))
    uuid = db.Column(db.String(11), db.ForeignKey('user.uuid', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref='student', cascade='all, delete', passive_deletes=True)

    def __init__(self):
        super(StudentInfo, self).__init__()

    def __init__(self, tup):
        self.stu_id = tup[0]
        self.stu_name = tup[1]
        self.phone_number = tup[2]
        self.email = tup[3]
        self.uuid = tup[4]

    def __repr__(self):
        return self.stu_id

    @property
    def serialize(self):
        return {
            'stu_id': self.stu_id,
            'stu_name': self.stu_name,
            'uuid': self.uuid,
        }


class TeacherInfo(db.Model):
    __tablename__ = 'teacher_info'

    teacher_id = db.Column(db.String(10), primary_key=True)
    teacher_name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(11))
    email = db.Column(db.String(30))
    uuid = db.Column(db.String(11), db.ForeignKey('user.uuid', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref='teacher', cascade='all, delete', passive_deletes=True)

    def __init__(self):
        super(TeacherInfo, self).__init__()

    def __init__(self, tup):
        self.teacher_id = tup[0]
        self.teacher_name = tup[1]
        self.phone_number = tup[2]
        self.email = tup[3]
        self.uuid = tup[4]

    def __repr__(self):
        return self.teacher_id

    @property
    def serialize(self):
        return {
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher_name,
            'uuid': self.uuid,
        }


class CourseInfo(db.Model):
    __tablename__ = 'course_info'

    course_id = db.Column(db.String(10), primary_key=True)
    course_name = db.Column(db.String(40), nullable=False)
    course_intro = db.Column(db.String(100))
    teacher_id = db.Column(db.String(10), db.ForeignKey('teacher_info.teacher_id', ondelete='CASCADE'), nullable=False)
    teacher = db.relationship('TeacherInfo', backref='course', cascade='all, delete', passive_deletes=True)

    def __init__(self):
        super(CourseInfo, self).__init__()

    def __init__(self, tup):
        self.course_id = tup[0]
        self.course_name = tup[1]
        self.course_intro = tup[2]
        self.teacher_id = tup[3]

    def __repr__(self):
        return self.course_id

    @property
    def serialize(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'teacher_id': self.teacher_id,
        }


class Sc(db.Model):
    __tablename__ = 'sc'

    course_id = db.Column(db.String(10), db.ForeignKey('course_info.course_id', ondelete='CASCADE'), primary_key=True,
                          nullable=False)
    stu_id = db.Column(db.String(10), db.ForeignKey('student_info.stu_id', ondelete='CASCADE'), primary_key=True,
                       nullable=False)
    course = db.relationship('CourseInfo', backref='sc', cascade='all, delete', passive_deletes=True)
    student = db.relationship('StudentInfo', backref='sc', cascade='all, delete', passive_deletes=True)

    def __init__(self):
        super(Sc, self).__init__()

    def __init__(self, tup):
        self.course_id = tup[0]
        self.stu_id = tup[1]

    @property
    def serialize(self):
        return {
            'course_id': self.course_id,
            'stu_id': self.stu_id,
        }


class CheckInTask(db.Model):
    __tablename__ = 'check_in_task'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.String(10), db.ForeignKey('course_info.course_id', ondelete='CASCADE'), nullable=False)
    course = db.relationship('CourseInfo', backref='task', cascade='all, delete', passive_deletes=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    # create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self):
        super(CheckInTask, self).__init__()

    def __init__(self, tup):
        self.task_id = tup[0]
        self.course_id = tup[1]
        self.start_time = tup[2]
        self.end_time = tup[3]

    def __repr__(self):
        return self.task_id

    @property
    def serialize(self):
        return {
            'task_id': self.task_id,
            'course_id': self.course_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
        }


class CheckInRecord(db.Model):
    __tablename__ = 'check_in_record'

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stu_id = db.Column(db.String(10), db.ForeignKey('student_info.stu_id', ondelete='CASCADE'), nullable=False)
    student = db.relationship('StudentInfo', backref='record', cascade='all, delete', passive_deletes=True)
    task_id = db.Column(db.Integer, db.ForeignKey('check_in_task.task_id', ondelete='CASCADE'), nullable=False)
    task = db.relationship('CheckInTask', backref='record', cascade='all, delete', passive_deletes=True)
    time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    idx_stu_id_task_id = UniqueConstraint('stu_id', 'task_id', name='idx_stu_id_task_id')

    def __init__(self):
        super(CheckInRecord, self).__init__()

    def __init__(self, tup):
        self.record_id = tup[0]
        self.stu_id = tup[1]
        self.task_id = tup[2]
        self.time = tup[3]

    def __repr__(self):
        return self.record_id

    @property
    def serialize(self):
        return {
            'record_id': self.record_id,
            'stu_id': self.stu_id,
            'task_id': self.task_id,
            'time': self.time,
        }


class Message(db.Model):
    time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, primary_key=True)
    body = db.Column(db.String(140))


    def __repr__(self):
        return '<Message {}>'.format(self.body)

    @property
    def serialize(self):
        return {
            'time': self.time,
            'body': self.body,
        }
