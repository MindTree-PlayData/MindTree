import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from mindtree.config import Config

app = Flask(__name__)
app.config.from_object(Config)

APP_PATH = os.path.dirname(__file__)  # 소문자 mindtree 경로를 의미함.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(APP_PATH, "key", "future-glider-321504-4b3a509617f3.json")


class Apps:
    analyzer = None


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)

from mindtree import routes
