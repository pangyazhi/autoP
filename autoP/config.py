import os
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRECT_KEY') or 'to be fixed later'
    WTF_CSRF_ENABLED = False
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5555
    SERVER_NAME = HOST + ':' + str(PORT)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    def __init__(self):
        pass

    SERVER_NAME = 'localhost:5000'
    DEBUG = True


class TestingConfig(Config):
    def __init__(self):
        pass

    TESTING = True


class ProductionConfig(Config):
    def __init__(self):
        pass

    PRODUCTION = True


config = dict(development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig,
              default=DevelopmentConfig)
