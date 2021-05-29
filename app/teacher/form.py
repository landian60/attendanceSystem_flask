from flask_admin.form import DatePickerWidget
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
from datetime import datetime


class CheckInTaskForm(FlaskForm):
    start_time = DateTimeField('签到开始时间', validators=[DataRequired()], default=datetime.now, format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField('签到结束时间', validators=[DataRequired()], default=datetime.now, format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('确认发布')


class EditInfoForm(FlaskForm):
    teacher_name = StringField('姓名', validators=[DataRequired(), Length(1, 20)])
    phone_number = StringField('电话', validators=[DataRequired(), Length(4, 11)])
    email = StringField('邮箱', validators=[DataRequired(), Length(5, 40)])
    submit = SubmitField('保存')


class CreateCourseForm(FlaskForm):
    course_id = StringField('课程号', validators=[DataRequired(), Length(1, 10)])
    course_name = StringField('课程名称', validators=[DataRequired(), Length(1, 40)])
    course_intro = StringField('课程简介', validators=[DataRequired(), Length(1, 100)])
    submit = SubmitField("创建")
