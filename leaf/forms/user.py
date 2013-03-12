#-*- coding:utf-8 -*-

from leaf.forms.common import ValidateInfo

class LoginForm():

    def __init__(self,username,password,email=''):
        self.username=username
        self.password=password
        self.email=email

    def validate(self):
        if self.username == '':
            return ValidateInfo(False,'username can not be null')
        if self.password == '':
            return ValidateInfo(False,'password can not be null')
        return ValidateInfo(True)

