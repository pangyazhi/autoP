import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRECT_KEY') or 'to be fixed later'
    WTF_CSRF_ENABLED = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    def __init__(self):
        pass

    SERVER_NAME = 'localhost:5000'
    DEBUG = True
    MONGOALCHEMY_DATABASE = 'Testing'
    MONGODB_SETTINGS = {'db': MONGOALCHEMY_DATABASE, 'host': 'mongodb://localhost/' + MONGOALCHEMY_DATABASE }
    DEBUG_TB_PANELS = ['flask.ext.mongoengine.panels.MongoDebugPanel']


class TestingConfig(Config):
    def __init__(self):
        pass

    TESTING = True
    SERVER_NAME = 'localhost:5000'
    MONGOALCHEMY_DATABASE = 'Testing'
    MONGODB_SETTINGS = {'db': MONGOALCHEMY_DATABASE, 'host': 'mongodb://localhost/' + MONGOALCHEMY_DATABASE}
    DEBUG_TB_PANELS = ['flask.ext.mongoengine.panels.MongoDebugPanel']


class ProductionConfig(Config):
    def __init__(self):
        pass

    PRODUCTION = True
    SERVER_NAME = '0.0.0.0:5000'
    MONGOALCHEMY_DATABASE = 'Automation'
    MONGODB_SETTINGS = {'db': MONGOALCHEMY_DATABASE, 'host': 'mongodb://localhost/' + MONGOALCHEMY_DATABASE}

config = dict(development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig,
              default=DevelopmentConfig)
