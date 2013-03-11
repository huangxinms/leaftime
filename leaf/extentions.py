#!/usr/bin/env python
#coding=utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from leaf import app

db = SQLAlchemy()
db.init_app(app)
db.app = app
