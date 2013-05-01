#-*- coding:utf-8 -*-

from flask import Flask
from leaf.corelib.flask_login import LoginManager,get_user_id


#-- create app --
app = Flask(__name__)
app.config.from_object('leaf.config')

app.jinja_env.globals.update(get_user_id=get_user_id)
app.jinja_env.globals.update(static='/static')

lm = LoginManager()
lm.init_app(app)

import views
