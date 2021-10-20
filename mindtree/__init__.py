import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from mindtree.config import Config

app = Flask(__name__)

APP_PATH = os.path.dirname(__file__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(APP_PATH, "../key", "future-glider-321504-4b3a509617f3.json")

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from mindtree import routes

    return app
