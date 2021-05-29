from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    user_type = SelectField('用户类型', validators=[DataRequired()],
                            choices=[('student', '学生'), ('teacher', '教师'), ('admin', '管理员')], default='student')
    user_id = StringField('学号/工号', validators=[DataRequired(), Length(1, 10)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    user_type = SelectField('用户类型', validators=[DataRequired()],
                            choices=[('student', '学生'), ('teacher', '教师')], default='student')
    user_id = StringField('学号/工号', validators=[DataRequired(), Length(1, 10)])
    password = PasswordField('密码',
                             validators=[DataRequired(), EqualTo('password2', message='两次密码必须匹配.')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')
