#!/usr/local/bin/python
#coding:utf-8

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:123@localhost/leaftime'
SECRET_KEY = '!@$leaftime!#$%^'
PORT = 5000
HOST = 'localhost'

try:
    from leaf.local_config import *
except:
    pass
