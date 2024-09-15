from app import login_manager

import bcrypt
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, logout_user, login_user

import app.model.user as user


auth_bp = Blueprint("auth_bp", __name__, template_folder="templates")


@login_manager.user_loader
def load_user(user_id):
    """
    Hydrates user object given a user id
    """
    return user.get_user_by_id(user_id)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = user.LoginForm()
    if form.validate_on_submit():
        if user.validate_login(form.username.data, form.password.data):
            u = user.get_user(form.username.data)
            if login_user(u):
                target = request.args.get("next")
                # TODO: Validate target url
                return redirect(target or url_for("admin_bp.index"))
        else:
            flash("Incorrect credentials, try again")
    return render_template("login_form.html", title="Login", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = user.RegisterForm()
    if form.validate_on_submit():
        if user.user_limit_reached():
            return "Thought you were real sneaky, huh? Guess what pal, this website ain't big enough for the two of us!"
        user.save_user(form.username.data, form.password.data)
        flash("YOURE REGISTERED")
        return redirect(url_for("auth_bp.login"))
    
    if user.user_limit_reached():
        return "There's only one user allowed and it's not YOU!"
    return render_template("login_form.html", title="Register", form=form)


def verify_password(plain_password, hashed_password) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_byte_enc, hashed_password)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))
