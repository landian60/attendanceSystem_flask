import random
import time

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models import *
from . import main


# 主页

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

# 公告栏
@main.route('/notice')
def notice():
    sql = "SELECT * FROM message;"
    _message = db.session.execute(sql)
    return render_template('notice.html',message=_message)


# 个人主页
@main.route('/my')
@login_required
def my():
    if current_user.user_type == 'student':
        return redirect(url_for('student.my'))
    elif current_user.user_type == 'teacher':
        return redirect(url_for('teacher.my'))
    elif current_user.user_type == 'admin':
        return redirect(url_for('admin.index'))


@main.route('/edit_info')
@login_required
def edit_info():
    if current_user.user_type == 'student':
        return redirect(url_for('student.edit_info'))
    elif current_user.user_type == 'teacher':
        return redirect(url_for('teacher.edit_info'))


# # 个人签到记录
# @main.route('/my/history')
# @login_required
# def my_history():
#     return render_template('my_history.html')


# # 课程签到统计查询
# @main.route('/manage/course/check_in')
# @login_required
# def manage_course_check_in():
#     return render_template('manage_course_check_in.html')


@main.route('/test/add_student')
def test_add_student():
    stu_id = request.args.get('stu_id')
    new_student = StudentInfo(stu_id=stu_id, stu_name=request.args.get('stu_name'),
                              password=request.args.get('password'))
    db.session.add(new_student)
    db.session.commit()
    return "Successfully add student(stu_id = " + stu_id + ")."


@main.route('/test/list_student')
def test_list_student():
    students = db.session.query(StudentInfo).all()
    return jsonify(students=[stu.serialize for stu in students])
