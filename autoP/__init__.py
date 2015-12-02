from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf import CsrfProtect
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = 'needtofixitlater'
app.config['SECRET_KEY'] = 'needtofixitlater'
app.config['WTF_CSRF_ENABLED'] = False
handler = RotatingFileHandler('app.log', maxBytes=1024000, backupCount=4)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
# login_manager.id_attribute = 'email'
login_manager.init_app(app)
csrf = CsrfProtect()
csrf.init_app(app)
Bootstrap(app)

import autoP.views
