from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class EditInfoForm(FlaskForm):
    stu_name = StringField('姓名', validators=[DataRequired(), Length(1, 20)])
    phone_number = StringField('电话', validators=[DataRequired(), Length(4, 11)])
    email = StringField('邮箱', validators=[DataRequired(), Length(5, 40)])
    submit = SubmitField('保存')


class CheckInForm(FlaskForm):
    task_id = StringField('签到任务编号', validators=[DataRequired(), Length(1, 10)])
    submit = SubmitField('确认签到')


class CourseInfoForm(FlaskForm):
    course_id = StringField('课程号', validators=[DataRequired(), Length(1, 10)])
    submit = SubmitField('确认')
