from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config.from_object("app.config.Config")
redis_client = FlaskRedis(app)

@app.route("/")
def healthcheck():
    return {"ping": "pong"}

@app.route("/redis-test")
def redis_test():
    redis_client.set("hello", "world")
    return redis_client.get("hello")
