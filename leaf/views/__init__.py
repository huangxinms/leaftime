#-*- coding:utf-8 -*-

from flask import g

from leaf import lm
from leaf import app
from leaf import config
from leaf.models.user_model import User

import user
import note

@lm.user_loader
def load_user(user_id):
    return User.query_obj.get_by_id(user_id)

@app.before_request
def before_request():
    g.config = config


@app.teardown_request
def teardown_request(exception):
    pass
