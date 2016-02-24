# -*- coding: utf-8 -*-
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from daya import flask_bcrypt
from flask.ext.login import (current_user, login_required)
import forms
import sys
from models import User
from flask.ext.paginate import Pagination

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

bp_user = Blueprint('bp_user', __name__, template_folder='templates')


@bp_user.route("/user/index", methods=["GET", "POST"])
@login_required
def index():
    index_form = request.form
    current_app.logger.info(request.form)
    search = False
    if not current_user.is_admin:
        return redirect('/')

    q = request.args.get('q')
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    user_obj = User()
    total = user_obj.get_count()
    users = user_obj.paginate(page, 8).items
    pagination = Pagination(css_framework='bootstrap3', link_size='sm', show_single_page=False,
                            page=page, per_page=8, total=total, search=search, record_name='users',
                            format_total=True, format_number=True)

    template_data = {
        'form': index_form,
        'users': users,
        'pagination': pagination
    }

    return render_template("/user/index.html", **template_data)


@bp_user.route("/user/create", methods=["GET", "POST"])
@login_required
def create():
    create_form = forms.UserCreateForm(request.form)
    current_app.logger.info(request.form)

    if request.method == 'POST' and not create_form.validate():
        current_app.logger.info(create_form.errors)
        # return "uhoh registration error"

    elif request.method == 'POST' and create_form.validate():
        name = create_form.uname.data
        account = create_form.account.data
        user_type = create_form.type.data
        # generate password hash
        password_hash = flask_bcrypt.generate_password_hash(create_form.password.data)

        # prepare User
        user = User(account, name, password_hash, user_type)
        user.address = create_form.address.data
        user.telephone = create_form.telephone.data
        user.description = create_form.description.data
        print user

        try:
            user.save()
            return redirect('/user/index')
        except Exception, e:
            print e
            flash(u'添加用户失败')
            current_app.logger.error(u'添加用户失败')

    # prepare registration form
    # registerForm = RegisterForm(csrf_enabled=True)
    template_data = {
        'form': create_form
    }

    return render_template("/user/create.html", **template_data)


@bp_user.route("/user/edit/<user_id>", methods=["GET", "POST"])
@login_required
def edit(user_id):
    current_app.logger.info(request.form)
    if user_id == 0:
        return
    user_obj = User()
    user = user_obj.get_by_id(user_id)
    edit_form = forms.UserEditForm(request.form, obj=user)
    # edit_form.populate_obj(user)
    if user is None:
        flash(u'无法找到有效用户')
        return

    if request.method == 'POST' and not edit_form.validate():
        current_app.logger.info(edit_form.errors)

    elif request.method == 'POST' and edit_form.validate():
        try:
            user.name = edit_form.name.data
            user.account = edit_form.account.data
            user.type = edit_form.type.data
            # generate password hash
            new_pass = request.form.get('pswdpop')
            if new_pass is not None and new_pass != "":
                user.password = flask_bcrypt.generate_password_hash(new_pass)
            user.address = edit_form.address.data
            user.telephone = edit_form.telephone.data
            user.description = edit_form.description.data
            print user

            user.save()
            return redirect('/user/index')

        except Exception, e:
            print e
            flash(u'编辑用户失败')
            current_app.logger.error(u'编辑用户失败')

    # prepare registration form
    # registerForm = RegisterForm(csrf_enabled=True)
    template_data = {
        'form': edit_form,
        'edit_user': user
    }

    return render_template("/user/edit.html", **template_data)


@bp_user.route("/user/show/<user_id>", methods=["GET", "POST"])
@login_required
def show(user_id):
    show_form = request.form
    current_app.logger.info(request.form)
    if user_id == 0:
        return
    user_obj = User()
    user = user_obj.get_by_id(user_id)
    if user is None:
        return

    template_data = {
        'form': show_form,
        'show_user': user
    }

    return render_template("/user/show.html", **template_data)


@bp_user.route("/user/delete/<user_id>", methods=["GET", "POST"])
@login_required
def delete(user_id):
    #delete_form = request.form
    current_app.logger.info(request.form)
    if user_id == 0:
        return
    user_obj = User()
    result = user_obj.delete(user_id)
    if not result:
        return

    return redirect('/user/index')

