import os
from app import create_app, db
from app.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

config_name = os.getenv('FLASK_CONFIG') or 'default'

app = create_app(config_name)
manager = Manager(app)
migrate = Migrate(app, db)

db.drop_all()
db.create_all()


def make_shell_context():
    return dict(app=app, db=db, User=User, StudentInfo=StudentInfo, TeacherInfo=TeacherInfo, CourseInfo=CourseInfo,
                CheckInTask=CheckInTask, CheckInRecord=CheckInRecord)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
