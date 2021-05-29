import pymysql

from config import *
from manage import config_name


class BaseDao:

    @staticmethod
    def init():
        conn = pymysql.connect(Config.DATABASE_HOST, Config.DATABASE_USERNAME, Config.DATABASE_PASSWORD,
                               config[config_name].DATABASE_NAME)
        cur = conn.cursor()
        return conn, cur

    @staticmethod
    def execute(sql, cur):
        print('sql:' + sql)
        cur.execute(sql)
        return cur

    @staticmethod
    def fetchone(sql, cur):
        cur = BaseDao.execute(sql, cur)
        return cur.fetchone()

    @staticmethod
    def fetchall(sql, cur):
        cur = BaseDao.execute(sql, cur)
        return cur.fetchall()

    @staticmethod
    def commit(conn):
        conn.commit()
        conn.close()
