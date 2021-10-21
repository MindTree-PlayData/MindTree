import os

class Config:
    SECRET_KEY = "donkey_secret"  # flash 쓰려면 설정해야함.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class PathConfig:
    APP_PATH = os.path.dirname(__file__)
    MEDIA_PATH = os.path.join(APP_PATH, "results")

