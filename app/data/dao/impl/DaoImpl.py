from app import myUtils
from app.data.bean.teacher_bean import *
from app.data.dao.BaseDao import BaseDao
from app.data.dao.StudentDao import StudentDao
from app.data.dao.TeacherDao import TeacherDao
from app.models import *
from app.data.bean.student_bean import *

from app.data.bean.student_bean import *


class DaoImpl(BaseDao, StudentDao, TeacherDao):

    @staticmethod
    def query_teacher_by_uuid(uuid):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM teacher_info WHERE uuid=\'" + uuid + "\';"
        _teacher = BaseDao.fetchone(sql, cur)
        BaseDao.commit(conn)
        if _teacher:
            return TeacherInfo(_teacher)
        else:
            return None

    @staticmethod
    def query_teacher_by_teacher_id(teacher_id):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM teacher_info WHERE teacher_id=\'" + teacher_id + "\';"
        _teacher = BaseDao.fetchone(sql, cur)
        BaseDao.commit(conn)
        if _teacher:
            return TeacherInfo(_teacher)
        else:
            return None

    @staticmethod
    def query_student_by_uuid(uuid):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM student_info WHERE uuid=\'" + uuid + "\';"
        _student = BaseDao.fetchone(sql, cur)
        BaseDao.commit(conn)
        if _student:
            return StudentInfo(_student)
        else:
            return None

    @staticmethod
    def query_student_by_course_id(course_id):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM student_info WHERE stu_id IN (SELECT stu_id FROM sc WHERE course_id=\'" + course_id + "\');"
        _student_list = BaseDao.fetchall(sql, cur)
        BaseDao.commit(conn)
        return [StudentInfo(_student) for _student in _student_list]

    @staticmethod
    def query_student_by_task_id_and_course_id(task_id, course_id):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM student_info WHERE stu_id IN (SELECT stu_id FROM sc WHERE course_id=\'" + \
              course_id + "\') AND stu_id NOT IN (SELECT stu_id FROM check_in_record WHERE task_id=\'" + task_id + "\');"
        _student_list = BaseDao.fetchall(sql, cur)
        BaseDao.commit(conn)
        return [StudentInfo(_student) for _student in _student_list]

    @staticmethod
    def query_course_by_teacher_id(teacher_id):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM course_info WHERE teacher_id=\'" + teacher_id + "\';"
        _course_list = BaseDao.fetchall(sql, cur)
        BaseDao.commit(conn)
        return [CourseInfo(_course) for _course in _course_list]

    @staticmethod
    def query_course_by_stu_id(stu_id):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM course_info AS cou, teacher_info AS tea WHERE cou.course_id IN (SELECT course_id FROM sc WHERE stu_id=\'" + stu_id + "\') AND cou.teacher_id=tea.teacher_id;"
        _course_list = BaseDao.fetchall(sql, cur)
        BaseDao.commit(conn)
        return [CourseInfoForStudent(_course) for _course in _course_list]

    @staticmethod
    def query_course_not_taken_by_stu_id(stu_id):
        conn, cur = BaseDao.init()
        sql = "SELECT course_id, course_name, course_info.teacher_id,teacher_name FROM course_info,teacher_info WHERE course_id NOT IN (SELECT course_id FROM sc WHERE stu_id=\'" + stu_id + "\');"
        _course_list = BaseDao.fetchall(sql, cur)
        BaseDao.commit(conn)
        return [CourseInfoForStudent(_course) for _course in _course_list]

    @staticmethod
    def query_course_by_course_id(course_id):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM course_info WHERE course_id=\'" + course_id + "\';"
        _course = BaseDao.fetchone(sql, cur)
        BaseDao.commit(conn)
        if _course:
            return CourseInfo(_course)
        else:
            return None

    @staticmethod
    def query_task_by_course_id(course_id):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM check_in_task WHERE course_id=\'" + course_id + "\' ORDER BY end_time DESC;"
        _task_list = BaseDao.fetchall(sql, cur)
        BaseDao.commit(conn)
        return [CheckInTask(_task) for _task in _task_list]

    @staticmethod
    def query_task_by_task_id(task_id):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM check_in_task WHERE task_id=\'" + task_id + "\';"
        _task = BaseDao.fetchone(sql, cur)
        BaseDao.commit(conn)
        return CheckInTask(_task)

    @staticmethod
    def query_task_by_course_id_and_now_time(course_id):
        conn, cur = BaseDao.init()
        now_time = datetime.now()
        sql = "SELECT task_id, course_id, start_time, end_time FROM check_in_task WHERE course_id=\'" + course_id + "\' AND start_time<=\'" + myUtils.datetime_for_sql(
            now_time) + "\' AND end_time>=\'" + myUtils.datetime_for_sql(now_time) + "\' ORDER BY end_time DESC;"
        _task = BaseDao.fetchone(sql, cur)
        BaseDao.commit(conn)
        if _task:
            return CheckInTask(_task)
        else:
            return None

    @staticmethod
    def query_check_in_record_for_teacher_by_task_id_and_course_id(task_id, course_id):
        conn, cur = BaseDao.init()
        sql = "SELECT stu.stu_id, stu.stu_name, time FROM student_info AS stu, check_in_record AS rec WHERE rec.task_id=\'" + task_id + "\' AND rec.stu_id IN (SELECT stu_id FROM sc WHERE course_id=\'" + \
              course_id + "\') AND stu.stu_id=rec.stu_id;"
        _record_list = BaseDao.fetchall(sql, cur)
        BaseDao.commit(conn)
        return [CheckInRecordForTeacher(_record) for _record in _record_list]

    @staticmethod
    def query_check_in_record_by_task_id_and_uuid(task_id, uuid):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM check_in_record WHERE stu_id=\'" + uuid + "\' AND task_id=\'" + str(
            task_id) + "\';"
        _record = BaseDao.fetchone(sql, cur)
        BaseDao.commit(conn)
        if _record:
            return CheckInRecord(_record)
        else:
            return None

    @staticmethod
    def query_check_in_record_by_stu_id(stu_id):
        conn, cur = BaseDao.init()
        sql = "SELECT cou.course_id, cou.course_name, rec.time FROM course_info AS cou, check_in_record AS rec, check_in_task AS task WHERE rec.stu_id=\'" + stu_id + "\' AND rec.task_id=task.task_id AND task.course_id=cou.course_id ORDER BY rec.time DESC;"
        record_list = BaseDao.fetchall(sql, cur)
        BaseDao.commit(conn)
        return [CheckInRecordForStudent(_record) for _record in record_list]

    @staticmethod
    def query_sc_by_course_id_and_stu_id(course_id, stu_id):
        conn, cur = BaseDao.init()
        sql = "SELECT * FROM sc WHERE course_id=\'" + course_id + "\' AND stu_id=\'" + stu_id + "\';"
        _sc = BaseDao.fetchone(sql, cur)
        BaseDao.commit(conn)
        if _sc:
            return Sc(_sc)
        else:
            return None

    @staticmethod
    def add_teacher(uuid, teacher_id, teacher_name, phone_number, email):
        conn, cur = BaseDao.init()
        sql = "INSERT INTO teacher_info VALUES (\'" + teacher_id + "\', \'" + teacher_name + "\', \'" + phone_number + "\', \'" + email + "\', \'" + uuid + "\');"
        BaseDao.execute(sql, cur)
        BaseDao.commit(conn)

    @staticmethod
    def update_teacher_by_uuid(uuid, teacher_name, phone_number, email):
        conn, cur = BaseDao.init()
        sql = "UPDATE teacher_info SET teacher_name=\'" + teacher_name + "\', phone_number=\'" + phone_number + "\', email=\'" + email + "\' WHERE uuid=\'" + uuid + "\';"
        BaseDao.execute(sql, cur)
        BaseDao.commit(conn)

    @staticmethod
    def update_student_by_uuid(uuid, stu_name, phone_number, email):
        conn, cur = BaseDao.init()
        sql = "UPDATE student_info SET stu_name=\'" + stu_name + "\', phone_number=\'" + phone_number + "\', email=\'" + email + "\' WHERE uuid=\'" + uuid + "\';"
        BaseDao.execute(sql, cur)
        BaseDao.commit(conn)

    @staticmethod
    def add_student(uuid, stu_id, stu_name, phone_number, email):
        conn, cur = BaseDao.init()
        sql = "INSERT INTO student_info VALUES (\'" + stu_id + "\', \'" + stu_name + "\', \'" + phone_number + "\', \'" + email + "\', \'" + uuid + "\');"
        BaseDao.execute(sql, cur)
        BaseDao.commit(conn)

    @staticmethod
    def add_course(course_id, course_name, course_intro, teacher_id):
        conn, cur = BaseDao.init()
        sql = "INSERT INTO course_info VALUES (\'" + course_id + "\', \'" + course_name + "\', \'" + course_intro + "\', \'" + teacher_id + "\');"
        BaseDao.execute(sql, cur)
        BaseDao.commit(conn)

    @staticmethod
    def add_check_in_task(course_id, start_time, end_time):
        conn, cur = BaseDao.init()
        sql = "INSERT INTO check_in_task(course_id, start_time, end_time) VALUES (\'" + course_id + "\', \'" + myUtils.datetime_for_sql(
            start_time) + "\', \'" + myUtils.datetime_for_sql(end_time) + "\');"
        BaseDao.execute(sql, cur)
        BaseDao.commit(conn)

    @staticmethod
    def add_check_in_record(stu_id, task_id):
        conn, cur = BaseDao.init()
        now_time = datetime.now()
        sql = "INSERT INTO check_in_record(stu_id, task_id, time) VALUES (\'" + stu_id + "\', \'" + task_id + "\', \'" + myUtils.datetime_for_sql(
            now_time) + "\');"
        BaseDao.execute(sql, cur)
        BaseDao.commit(conn)

    @staticmethod
    def add_sc_by_course_id_and_stu_id(course_id, stu_id):
        conn, cur = BaseDao.init()
        sql = "INSERT INTO sc VALUES (\'" + str(course_id) + "\', \'" + stu_id + "\');"
        BaseDao.execute(sql, cur)
        BaseDao.commit(conn)

    @staticmethod
    def delete_sc_by_course_id_and_stu_id(course_id, stu_id):
        conn, cur = BaseDao.init()
        sql = "DELETE FROM sc WHERE course_id=\'" + str(course_id) + "\' AND stu_id=\'" + stu_id + "\';"
        BaseDao.execute(sql, cur)
        BaseDao.commit(conn)
