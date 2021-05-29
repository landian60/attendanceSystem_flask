import pymysql
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import myUtils
from config import *
from app.models import *
from manage import config_name
from . import student

from .form import *
from app.data.dao.impl.DaoImpl import DaoImpl

USER_TYPE = 'student'
HOME_PAGE = 'main.index'
NO_PERMISSION_TEXT = '没有访问权限.'
CHECK_IN_HOST = '127.0.0.1'
CHECK_IN_PORT = '5000'
CHECK_IN_TYPE = 'student/check_in/'
CHECK_IN_URL_HEAD = 'http://' + CHECK_IN_HOST + ':' + CHECK_IN_PORT + '/' + CHECK_IN_TYPE

# 个人主页
@student.route('/my')
@login_required
def my():
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    uuid = current_user.uuid
    print('uuid:' + uuid)
    student = DaoImpl.query_student_by_uuid(uuid)
    # 不存在该学生信息
    if student is None:
        flash('请完善个人信息.')
        return redirect(url_for('student.edit_info'))
    course_list = DaoImpl.query_course_by_stu_id(student.stu_id)
    return render_template('student/my.html', student=student, course_list=course_list)


# 个人信息编辑页面
@student.route('/edit_info', methods=['GET', 'POST'])
@login_required
def edit_info():
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    uuid = current_user.uuid
    stu_id = myUtils.get_user_id(uuid)
    form = EditInfoForm()
    if form.validate_on_submit():
        stu_name = form.stu_name.data
        phone_number = form.phone_number.data
        email = form.email.data
        student = DaoImpl.query_student_by_uuid(uuid)
        # 不存在该学生信息，插入
        if student is None:
            DaoImpl.add_student(uuid, stu_id, stu_name, phone_number, email)
        # 存在该学生信息，修改
        else:
            DaoImpl.update_student_by_uuid(uuid, stu_name, phone_number, email)
        flash('编辑成功.')
        return redirect(url_for('student.my'))
    return render_template('student/edit_info.html', stu_id=stu_id, form=form)


# 加入课程
@student.route('/join_course', methods=['GET', 'POST'])
@login_required
def join_course():
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    uuid = current_user.uuid
    stu_id = myUtils.get_user_id(uuid)
    if request.method == 'POST':
        # 加入课程
        data = request.get_json()
        course_id = data['course_id']
        DaoImpl.add_sc_by_course_id_and_stu_id(course_id, stu_id)
        flash('成功加入课程.')
        return jsonify({'result': 'ok'})

    # 获取未修读课程
    course_list = DaoImpl.query_course_not_taken_by_stu_id(stu_id)
    return render_template('student/join_course.html', course_list=course_list)


# 退出课程
@student.route('/quit_course', methods=['POST'])
@login_required
def quit_course():
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    uuid = current_user.uuid
    stu_id = myUtils.get_user_id(uuid)
    data = request.get_json()
    course_id = data['course_id']
    DaoImpl.delete_sc_by_course_id_and_stu_id(course_id, stu_id)
    flash('已退出课程.')
    return jsonify({'result': 'ok'})


# 签到页面
@student.route('/check_in/<course_id>', methods=['GET', 'POST'])
@login_required
def check_in(course_id):
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    uuid = current_user.uuid
    stu_id = myUtils.get_user_id(uuid)
    now_time = datetime.now()
    form = CheckInForm()
    if form.validate_on_submit():
        task_id = form.task_id.data
        task = DaoImpl.query_task_by_task_id(task_id)
        if task.end_time >= now_time:
            # 签到
            DaoImpl.add_check_in_record(stu_id, task_id)
            flash('签到成功.')
        else:
            # 拒绝签到
            flash('签到失败：不在签到时段.')
        return redirect(url_for('student.check_in', course_id=course_id))

    else:
        task_value = False
        sc = DaoImpl.query_sc_by_course_id_and_stu_id(course_id, stu_id)
        if sc is None:
            # 未修读此门课程
            flash('你未修读此门课程，无法签到.')
            return redirect(url_for(HOME_PAGE))
        task = DaoImpl.query_task_by_course_id_and_now_time(course_id)
        if task is None:
            print("task:null")
            flash('当前不在签到时段.')
        else:
            record = DaoImpl.query_check_in_record_by_task_id_and_uuid(task.task_id, myUtils.get_user_id(current_user.uuid))
            if record is None:
                # 未签到
                task_value = False
            else:
                # 已签到
                task_value = True
        course = DaoImpl.query_course_by_course_id(course_id)
        course_name = course.course_name
        teacher_id = course.teacher_id
        teacher = DaoImpl.query_teacher_by_teacher_id(teacher_id)
        teacher_name = teacher.teacher_name
        return render_template('student/check_in.html', course_id=course_id, course_name=course_name,
                               teacher_name=teacher_name, task=task, form=form, task_value=task_value)


# 查看签到记录页面
@student.route('/list_check_in_record')
@login_required
def list_check_in_record():
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    uuid = current_user.uuid
    stu_id = myUtils.get_user_id(uuid)
    record_list = DaoImpl.query_check_in_record_by_stu_id(stu_id)
    return render_template('student/list_check_in_record.html', record_list=record_list)
