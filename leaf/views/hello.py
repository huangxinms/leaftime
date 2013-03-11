#-*- coding:utf-8 -*-
from flask import g,render_template,Module
from leaf import app
from leaf.models.user_model import User

@app.route('/hello',methods=['GET'])
def hello():
    User.query_obj.get_by_username('huangxin').set_email('huangxinms@gmail.com')
    print User.query_obj.get_by_username('huangxin').get_email()
    return render_template('hello.html')
