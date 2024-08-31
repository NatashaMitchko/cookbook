from app import login_manager
from app import redis_client

from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user


auth_bp = Blueprint("auth_bp", __name__, template_folder="templates")


@login_manager.user_loader
def load_user(user_id):
    """
    Hydrates user object given a user id
    """
    return redis_client.get(user_id)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # TODO
    pass


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("TODO"))
