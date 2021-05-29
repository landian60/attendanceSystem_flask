import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DATABASE_HOST = '127.0.0.1'
    DATABASE_USERNAME = 'root'
    DATABASE_PASSWORD = '123456'
    # FLASK_ADMIN_SWATCH = 'cerulean'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_NAME = 'attendance_dev'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + Config.DATABASE_USERNAME + ':' + Config.DATABASE_PASSWORD + '@' + Config.DATABASE_HOST + ':3306/' + DATABASE_NAME


class TestingConfig(Config):
    TESTING = True
    DATABASE_NAME = 'attendance_test'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + Config.DATABASE_USERNAME + ':' + Config.DATABASE_PASSWORD + '@' + Config.DATABASE_HOST + ':3306/' + DATABASE_NAME


class ProductionConfig(Config):
    DATABASE_NAME = 'attendance_dev'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + Config.DATABASE_USERNAME + ':' + Config.DATABASE_PASSWORD + '@' + Config.DATABASE_HOST + ':3306/' + DATABASE_NAME


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
