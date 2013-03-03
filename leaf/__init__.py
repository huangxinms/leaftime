#-*- coding:utf-8 -*-

from flask import Flask

#-- create app --
app = Flask(__name__)
app.config.from_object('leaf.config')

import views
