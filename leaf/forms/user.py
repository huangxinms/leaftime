#-*- coding:utf-8 -*-

from leaf.corelib.mail import check_email
from leaf.forms.common import ValidateInfo
from leaf.models.user_model import User, UserRegist

class LoginForm():

    def __init__(self, email, password, username=''):
        self.email = email
        self.password = password
        self.username = username

    def validate(self):
        if self.email == '':
            return ValidateInfo(False, u'邮箱不能为空')
        if self.password == '':
            return ValidateInfo(False, u'密码不能为空')
        return ValidateInfo(True)

class RegistForm():

    def __init__(self, email):
        self.email = email

    def validate(self):
        if self.email == '':
            return ValidateInfo(False, u'邮箱不能为空')
        if not check_email(self.email):
            return ValidateInfo(False, u'请输入合法的邮箱地址')
        return ValidateInfo(True)


class RegistPasswordForm():

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def validate(self):
        if self.email == '':
            return ValidateInfo(False, u'邮箱不能为空')
        if not check_email(self.email):
            return ValidateInfo(False, u'请输入合法的邮箱地址')
        user = User.query_obj.get_by_email(self.email)
        if user:
            return ValidateInof(False, u'该邮箱已经被注册')
        return ValidateInfo(True)

class ChangePasswordForm():

    def __init__(self, new_password, confirm_password):
        self.new_password = new_password
        self.confirm_password = confirm_password

    def validate(self):
        if self.new_password != self.confirm_password:
            return ValidateInfo(False, u'两次密码输入不一致')
        return ValidateInfo(True)
