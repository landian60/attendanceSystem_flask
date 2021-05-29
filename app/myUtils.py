from datetime import datetime


def get_uuid(id, user_type):
    if user_type == 'student':
        return '0' + id
    elif user_type == 'teacher':
        return '1' + id
    elif user_type == 'admin':
        return '2' + id


def get_user_id(uuid):
    return uuid[1:]


def datetime_for_sql(my_datetime):
    return my_datetime.strftime("%Y-%m-%d %H:%M:%S")


def now_datetime_for_sql():
    return datetime_for_sql(datetime.now())
