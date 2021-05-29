import qrcode
import base64
import io
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import myUtils
from app.data.dao.impl.DaoImpl import DaoImpl
from config import *
from manage import config_name
from . import teacher

# 个人主页
from .form import CheckInTaskForm, EditInfoForm, CreateCourseForm

USER_TYPE = 'teacher'
HOME_PAGE = 'main.index'
NO_PERMISSION_TEXT = '没有访问权限.'


@teacher.route('/my')
@login_required
def my():
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    uuid = current_user.uuid
    print('uuid:' + uuid)
    teacher = DaoImpl.query_teacher_by_uuid(uuid)
    # 不存在该教师信息
    if teacher is None:
        flash('请完善个人信息.')
        return redirect(url_for('teacher.edit_info'))
    # 获取课程列表
    course_list = DaoImpl.query_course_by_teacher_id(teacher.teacher_id)

    return render_template('teacher/my.html', teacher=teacher, course_list=course_list)


# 个人信息编辑页面
@teacher.route('/edit_info', methods=['GET', 'POST'])
@login_required
def edit_info():
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    uuid = current_user.uuid
    teacher_id = myUtils.get_user_id(uuid)
    form = EditInfoForm()
    if form.validate_on_submit():
        teacher_name = form.teacher_name.data
        phone_number = form.phone_number.data
        email = form.email.data
        teacher = DaoImpl.query_teacher_by_uuid(uuid)
        # 存在该教师信息，修改
        if teacher:
            DaoImpl.update_teacher_by_uuid(uuid, teacher_name, phone_number, email)
        # 不存在该教师信息，插入
        else:
            DaoImpl.add_teacher(uuid, teacher_id, teacher_name, phone_number, email)
        flash('编辑成功.')
        return redirect(url_for('teacher.my'))

    return render_template('teacher/edit_info.html', teacher_id=teacher_id, form=form)


# 创建课程
@teacher.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    uuid = current_user.uuid
    teacher_id = myUtils.get_user_id(uuid)
    form = CreateCourseForm()
    if form.validate_on_submit():
        course_id = form.course_id.data
        course_name = form.course_name.data
        course_intro = form.course_intro.data
        DaoImpl.add_course(course_id, course_name, course_intro, teacher_id)
        flash('课程创建成功.')
        return redirect(url_for('teacher.my'))

    return render_template('teacher/create_course.html', form=form)


# 查看选课学生名单
@teacher.route('/list_student/<course_id>')
@login_required
def list_student(course_id):
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    course = DaoImpl.query_course_by_course_id(course_id)
    student_list = DaoImpl.query_student_by_course_id(course_id)

    return render_template('teacher/list_student.html', course=course, student_list=student_list)


# 查看签到任务
@teacher.route('/list_check_in/<course_id>')
@login_required
def list_check_in(course_id):
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    course = DaoImpl.query_course_by_course_id(course_id)
    task_list = DaoImpl.query_task_by_course_id(course_id)
    return render_template('teacher/list_check_in.html', task_list=task_list, course=course)


# 查看签到情况
@teacher.route('/list_check_in_student/<task_id>')
@login_required
def list_check_in_student(task_id):
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    task = DaoImpl.query_task_by_task_id(task_id)
    course = DaoImpl.query_course_by_course_id(task.course_id)
    check_in_stu_list = DaoImpl.query_check_in_record_for_teacher_by_task_id_and_course_id(task_id,
                                                                                           task.course_id)
    uncheck_in_stu_list = DaoImpl.query_student_by_task_id_and_course_id(task_id, task.course_id)
    return render_template('teacher/list_check_in_student.html', task=task, course=course,
                           check_in_stu_list=check_in_stu_list, uncheck_in_stu_list=uncheck_in_stu_list)


# 发布签到任务
@teacher.route('/create_check_in/<course_id>', methods=['GET', 'POST'])
@login_required
def create_check_in(course_id):
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    form = CheckInTaskForm()
    if form.validate_on_submit():
        print(type(form.start_time))
        start_time = form.start_time.data
        end_time = form.end_time.data
        DaoImpl.add_check_in_task(course_id, start_time, end_time)
        flash('发布成功.')
        return redirect(url_for('teacher.list_check_in', course_id=course_id))

    course = DaoImpl.query_course_by_course_id(course_id)
    return render_template('teacher/create_check_in.html', form=form, course=course)


# 查看签到二维码
@teacher.route('/check_in_code/<course_id>')
@login_required
def check_in_code(course_id):
    if current_user.user_type != USER_TYPE:
        flash(NO_PERMISSION_TEXT)
        return redirect(url_for(HOME_PAGE))
    course = DaoImpl.query_course_by_course_id(course_id)
    # 二维码
    check_in_url = url_for('student.check_in', course_id=course_id, _external=True)
    img = qrcode.make(check_in_url)
    # creates qrcode base64
    out = io.BytesIO()
    img.save(out, 'PNG')
    img_stream = u"data:image/png;base64," + base64.b64encode(out.getvalue()).decode('ascii')

    return render_template('teacher/check_in_code.html', img_stream=img_stream, course=course)
