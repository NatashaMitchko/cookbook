from app import login_manager
from app import redis_client

import bcrypt
from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, logout_user

from app.model.user import LoginForm


auth_bp = Blueprint("auth_bp", __name__, template_folder="templates")


@login_manager.user_loader
def load_user(user_id):
    """
    Hydrates user object given a user id
    """
    return redis_client.get(user_id)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO
        return redirect(url_for("admin_bp.index"))
    return render_template("login_form.html", title="Login", form=form)

def verify_password(plain_password, hashed_password) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_byte_enc, hashed_password)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("recipe_bp.index"))
