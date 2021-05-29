from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required

from app import db, myUtils
from app.auth.form import LoginForm, RegistrationForm
from app.models import User
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_type = form.user_type.data
        user_id = form.user_id.data
        if user_type == 'admin':
            return redirect(url_for('admin.index'))
        user = User.query.filter_by(uuid=myUtils.get_uuid(user_id, user_type)).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('帐号或密码错误.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录成功.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = form.password.data
        user_type = form.user_type.data
        user_id = form.user_id.data
        uuid = myUtils.get_uuid(user_id, user_type)
        if User.query.filter_by(uuid=uuid).first():
            flash('该学号/工号已注册.')
        else:
            user = User(uuid=uuid, password=password, user_type=user_type)
            db.session.add(user)
            db.session.commit()
            flash('注册成功.')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
