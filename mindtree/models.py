from datetime import datetime
from mindtree import db


class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # 해당 유저의 모든 포스트 연결

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ocr_text = db.Column(db.String(100), nullable=False)
    sentiment = db.Column(db.JSON, nullable=False)
    word_cloud_path = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.user_id}', '{self.pub_date}', '{self.ocr_text}'," \
               f" '{self.sentiment}', '{self.word_cloud_path}')"

