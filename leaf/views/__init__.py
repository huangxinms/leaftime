#-*- coding:utf-8 -*-
from flask import g

from leaf import app
from leaf import config

import hello
import user


@app.before_request
def before_request():
    g.config = config


@app.teardown_request
def teardown_request(exception):
    pass
