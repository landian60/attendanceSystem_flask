from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_admin import Admin, AdminIndexView

from app.admin.model_views import MyModelView

bootstrap = Bootstrap()
db = SQLAlchemy()


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    admin = Admin(app, name='Attendance', template_mode='bootstrap3')
    from app.models import User
    admin.add_view(MyModelView(User, db.session))
    from app.models import StudentInfo
    admin.add_view(MyModelView(StudentInfo, db.session))
    from app.models import TeacherInfo
    admin.add_view(MyModelView(TeacherInfo, db.session))
    from app.models import Sc
    admin.add_view(MyModelView(Sc, db.session))
    from app.models import CourseInfo
    admin.add_view(MyModelView(CourseInfo, db.session))
    from app.models import CheckInTask
    admin.add_view(MyModelView(CheckInTask, db.session))
    from app.models import CheckInRecord
    admin.add_view(MyModelView(CheckInRecord, db.session))
    from app.models import Message
    admin.add_view(MyModelView(Message, db.session))


    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .student import student as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/student')

    from .teacher import teacher as teacher_blueprint
    app.register_blueprint(teacher_blueprint, url_prefix='/teacher')

    app.app_context().push() #同时推送app的程序上下文环境

    return app
