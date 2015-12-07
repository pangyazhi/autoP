from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf import CsrfProtect
import logging
from logging.handlers import RotatingFileHandler
from config import config


handler = RotatingFileHandler('app.log', maxBytes=1024000, backupCount=4)
handler.setLevel(logging.INFO)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
csrf = CsrfProtect()
app = Flask(__name__)


def create_app(config_name):

    app.config.from_object(config[config_name])
    app.logger.addHandler(handler)
    login_manager.init_app(app)
    csrf.init_app(app)
    Bootstrap(app)
    return app


from . import views



