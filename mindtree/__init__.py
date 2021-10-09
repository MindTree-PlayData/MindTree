from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from mindtree.utils.OCR import ocr
from mindtree.utils.request_sentiment import sentiment_analysis
from mindtree.utils.text_analysis import text_mining

app = Flask(__name__)
app.config['SECRET_KEY'] = "donkey_secret"  # flash 쓰려면 설정해야함.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# db.init_app(app)

from mindtree import routes
