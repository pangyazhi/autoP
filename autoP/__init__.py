from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf import CsrfProtect
import logging
from logging.handlers import RotatingFileHandler
from config import config
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension
from mongoengine import connect


handler = RotatingFileHandler('app.log', maxBytes=1024000, backupCount=4)
handler.setLevel(logging.INFO)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
csrf = CsrfProtect()
app = Flask(__name__)
db = MongoEngine()


def create_app(config_name):

    app.config.from_object(config[config_name])
    app.logger.addHandler(handler)
    login_manager.init_app(app)
    csrf.init_app(app)
    Bootstrap(app)
    db.init_app(app)
    # toolbar = DebugToolbarExtension(app)
    # app.session_interface = MongoEngineSessionInterface(db)
    return app


def delete_db():
    db_name = app.config.get('MONGOALCHEMY_DATABASE')
    connect(db_name).drop_database(db_name)
    return True

from . import views



