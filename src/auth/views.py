# -*- coding: utf-8 -*-
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from daya import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

from user.models import User

bp_auth = Blueprint('bp_auth', __name__, template_folder='templates')


# noinspection PyUnresolvedReferences
@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "j_username" in request.form:
        name = request.form["j_username"]
        user_obj = User()
        user = user_obj.get_by_name_w_password(name)
        if user and flask_bcrypt.check_password_hash(user.password, request.form["j_password"]) and user.is_valid():
            remember = request.form.get("remember", "no") == "yes"

            if login_user(user, remember=remember) and user.type == 1:
                return redirect('/device/index')
            else:
                flash("登录失败")

    return render_template("/auth/login.html")


@bp_auth.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        return redirect(request.args.get("next") or '/admin')

    template_data = {}
    return render_template("/auth/reauth.html", **template_data)


@bp_auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_user(id):
    if id is None:
        redirect('/login')
    user = User()
    user.get_by_id(id)
    if user.is_active():
        return user
    else:
        return None
