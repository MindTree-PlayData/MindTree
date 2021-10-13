import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "donkey_secret"  # flash 쓰려면 설정해야함.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP_PATH = os.path.dirname(__file__)
USER_BASE_PATH = os.path.join(APP_PATH, "results")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(APP_PATH, "../key", "future-glider-321504-4b3a509617f3.json")
db = SQLAlchemy(app)
# db.init_app(app)

from mindtree import routes
