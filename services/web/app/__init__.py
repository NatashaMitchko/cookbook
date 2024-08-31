from flask import Flask
from flask_redis import FlaskRedis
from flask_login import LoginManager
import json

redis_client = FlaskRedis()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    redis_client.init_app(app)
    login_manager.init_app(app)

    from app.blueprints.auth.routes import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.blueprints.admin.routes import admin_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.blueprints.recipes.routes import recipe_bp

    app.register_blueprint(recipe_bp, url_prefix="/recipe")

    return app


app = create_app()


@app.route("/")
def healthcheck():
    return {"ping": "pong"}


@app.route("/redis-test")
def redis_test():
    redis_client.set("hello", json.dumps({"hello": "world"}))
    return redis_client.get("hello")
