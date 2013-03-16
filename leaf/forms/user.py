#-*- coding:utf-8 -*-

from leaf.forms.common import ValidateInfo

class LoginForm():

    def __init__(self, email, password, username=''):
        self.email=email
        self.password=password
        self.username=username

    def validate(self):
        if self.email== '':
            return ValidateInfo(False, u'邮箱不能为空')
        if self.password == '':
            return ValidateInfo(False, u'密码不能为空')
        return ValidateInfo(True)

