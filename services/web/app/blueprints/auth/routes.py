from app import login_manager

import bcrypt
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, logout_user, login_user

import app.model.user as user
import app.model.forms as forms

from app.utility.http import url_has_allowed_host_and_scheme


auth_bp = Blueprint("auth_bp", __name__, template_folder="templates")


@login_manager.user_loader
def load_user(user_id):
    return user.get_user_by_id(user_id)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        if user.validate_login(form.username.data, form.password.data):
            u = user.get_user(form.username.data)
            if login_user(u):
                target = request.args.get("next")
                if not url_has_allowed_host_and_scheme(target, request.host):
                    return redirect(url_for("admin_bp.index"))
                return redirect(target or url_for("admin_bp.index"))
            else:
                flash("login_user failed")
        else:
            flash("Incorrect credentials, try again")
    return render_template("login_form.html", title="Login", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        if user.user_limit_reached():
            return "Thought you were real sneaky, huh? Guess what pal, this website ain't big enough for the two of us!"
        user.save_user(form.username.data, form.password.data)
        flash("YOURE REGISTERED")
        return redirect(url_for("auth_bp.login"))

    if user.user_limit_reached():
        flash("There's only one user allowed and it's not YOU!")
        return redirect(url_for("admin_bp.index"))
    return render_template("login_form.html", title="Register", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))
