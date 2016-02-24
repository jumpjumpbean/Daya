# -*- coding: utf-8 -*-
import models
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *
from flask.ext.mongoengine.wtf.orm import validators

user_form = model_form(models.UserModel, exclude=['password'])


# Signup Form created from user_form
class UserCreateForm(user_form):
    password = PasswordField(u'密码', default='', validators=[validators.Required(message='密码不能为空')])
    account = StringField(u'登录账号', default='', validators=[validators.Required(message='登录账号不能为空')])
    uname = StringField(u'用户姓名', default='', validators=[validators.Required(message='用户姓名不能为空')])
    type = SelectField(u'用户类型', choices=[(0, u'办事处'), (1, u'总部')], coerce=int)
    # password = PasswordField('Password', validators=[validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    # confirm = PasswordField('Repeat Password')


class UserEditForm(user_form):
    pswdpop = PasswordField(u'新密码', default='')
    confirmpop = PasswordField(u'再次输入新密码', default='')
    account = StringField(u'登录账号', default='', validators=[validators.Required(message='登录账号不能为空')])
    name = StringField(u'用户姓名', default='', validators=[validators.Required(message='用户姓名不能为空')])
    type = SelectField(u'用户类型', choices=[(0, u'办事处'), (1, u'总部')], coerce=int)


# Login form will provide a Password field (WTForm form field)
class LoginForm(user_form):
    password = PasswordField('password', validators=[validators.Required()])
