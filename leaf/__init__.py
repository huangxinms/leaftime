#-*- coding:utf-8 -*-

from flask import Flask
from leaf.corelib.flask_login import LoginManager


#-- create app --
app = Flask(__name__)
app.config.from_object('leaf.config')

lm = LoginManager()
lm.init_app(app)

import views
