#!/usr/local/bin/python
#coding:utf-8

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql://root:123@localhost/leaftime'
SECRET_KEY = '!@$leaftime!#$%^'
PORT = 5000
HOST = 'localhost'

MAIL_HOST = ''
MAIL_PORT = ''
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

try:
    from leaf.local_config import *
except:
    pass
