import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("APP_SECRET_KEY")
    REDIS_URL = os.getenv("REDIS_URL")
