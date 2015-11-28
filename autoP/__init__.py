from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'need to fix it later'
app.config['SECRET_KEY'] = 'need to fix it later'

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
# login_manager.id_attribute = 'email'
login_manager.init_app(app)

import autoP.views
