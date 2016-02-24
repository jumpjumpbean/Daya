# -*- coding: utf-8 -*-
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from models import Device
from flask.ext.login import login_required
from flask.ext.paginate import Pagination


bp_device = Blueprint('bp_device', __name__, template_folder='templates')


@bp_device.route("/", methods=["GET", "POST"])
@bp_device.route("/device/index", methods=["GET", "POST"])
@login_required
def index():
    index_form = request.form
    current_app.logger.info(request.form)
    search = False

    q = request.args.get('q')
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    device_obj = Device()
    total = device_obj.get_count()
    devices = device_obj.paginate(page, 8).items
    pagination = Pagination(css_framework='bootstrap3', link_size='sm', show_single_page=False,
                            page=page, per_page=8, total=total, search=search, record_name='devices',
                            format_total=True, format_number=True)

    template_data = {
        'form': index_form,
        'devices': devices,
        'pagination': pagination
    }

    return render_template("/device/index.html", **template_data)


@bp_device.route("/device/create", methods=["GET", "POST"])
@login_required
def create():
    create_form = request.form
    current_app.logger.info(request.form)

    if request.method == 'POST':
        hospital = request.form['hospital']
        device_model = request.form['device_model']
        device_index = request.form['device_index']
        owner = request.form['owner']

        # prepare Device
        device = Device(hospital, device_model, device_index, owner)
        device.status = request.form['status']
        device.update_user = current_user.name
        print device

        try:
            device.save()
            return redirect('/device/index')

        except Exception, e:
            print e
            flash(u'添加维修部品失败')
            current_app.logger.error(u'添加维修部品失败')

    # prepare registration form
    # registerForm = RegisterForm(csrf_enabled=True)
    template_data = {

        'form': create_form
    }

    return render_template("/device/create.html", **template_data)


@bp_device.route("/device/edit/<device_id>", methods=["GET", "POST"])
@login_required
def edit(device_id):
    edit_form = request.form
    current_app.logger.info(request.form)
    if device_id == 0:
        return
    device_obj = Device()
    device = device_obj.get_by_id(device_id)
    if device is None:
        return

    if request.method == 'POST':
        try:
            device.hospital = request.form['hospital']
            device.device_model = request.form['device_model']
            device.device_index = request.form['device_index']
            device.owner = request.form['owner']
            device.status = request.form['status']
            device.update_user = request.form['update_user']
            print device
            device.save()
            return redirect('/device/index')

        except Exception, e:
            print e
            flash(u'编辑维修部品失败')
            current_app.logger.error(u'编辑维修部品失败')

    # prepare registration form
    # registerForm = RegisterForm(csrf_enabled=True)
    template_data = {
        'form': edit_form,
        'current_device': device
    }

    return render_template("/device/edit.html", **template_data)


@bp_device.route("/device/show/<device_id>", methods=["GET", "POST"])
@login_required
def show(device_id):
    show_form = request.form
    current_app.logger.info(request.form)
    if device_id == 0:
        return
    device_obj = Device()
    device = device_obj.get_by_id(device_id)
    if device is None:
        return

    template_data = {
        'form': show_form,
        'current_device': device
    }

    return render_template("/device/show.html", **template_data)


@bp_device.route("/device/delete/<device_id>", methods=["GET", "POST"])
@login_required
def delete(device_id):
    #delete_form = request.form
    current_app.logger.info(request.form)
    if device_id == 0:
        return
    device_obj = Device()
    result = device_obj.delete(device_id)
    if not result:
        return

    return redirect('/device/index')