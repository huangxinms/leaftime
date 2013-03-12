#-*- coding:utf-8 -*-
from flask import g,render_template,Module,request
from leaf import app
from leaf.models.user_model import User
from leaf.forms.user import LoginForm

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('hello.html')
    if request.method == 'POST':
        username = request.form['username']
        password = '1111'
        result = LoginForm(username=username,password=password).validate()
        if result.is_success:
            print 'success'
        else:
            print User.query_obj.get_by_username('huangxin').get_email()
    return render_template('hello.html')
