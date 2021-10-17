from datetime import datetime
from mindtree import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # id의 db.Integer는 자동증가 설정 안해줘도 primary_key면 자동 삽입됨.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # 해당 유저의 모든 포스트 연결

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 자동 증가
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 참조: 'author'키로
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 자동 입력됨
    ocr_text = db.Column(db.String(100), nullable=False)
    sentiment = db.Column(db.JSON, nullable=False)
    word_cloud = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.user_id}', '{self.pub_date}', '{self.ocr_text}'," \
               f" '{self.sentiment}', '{self.word_cloud}')"
