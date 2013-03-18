#-*- coding:utf-8 -*-

from flask import g,render_template,Module,request,redirect,flash,url_for
from leaf import app
from leaf.models.user_model import User
from leaf.forms.user import LoginForm

from leaf.corelib.flask_login import login_required,login_user

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = LoginForm(email=email, password=password).validate()
        if result.is_success:
            user = User.query_obj.get_by_email(email)
            if user is None:
                flash(u'该邮箱尚未注册')
            else:
                result = user.check(password)
                if result:
                    login_user(user)
                    return redirect(url_for('hello'))
                else:
                    flash(u'用户名或密码错误')
        else:
            flash(result.message)
    return redirect(url_for('login'))

@app.route('/regist',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
