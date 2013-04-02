#-*- coding:utf-8 -*-

from flask import render_template, request, redirect, flash, url_for

from leaf import app
from leaf.corelib.flask_login import login_user, logout_user, get_user_id
from leaf.models.user_model import User
from leaf.forms.user import LoginForm

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        user_id = get_user_id()
        if user_id:
            return redirect(url_for('latest'))
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = LoginForm(email=email, password=password).validate()
        # TODO: move password verification to form
        if result.is_success:
            user = User.query_obj.get_by_email(email)
            if user is None:
                flash(u'该邮箱尚未注册')
            else:
                result = user.check(password)
                if result:
                    login_user(user)
                    return redirect(url_for('latest'))
                else:
                    flash(u'用户名或密码错误')
        else:
            flash(result.message)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('register'))


@app.route('/register',methods=['GET','POST'])
@app.route('/')
def register():
    if request.method == 'GET':
        user_id = get_user_id()
        if user_id != 0:
            return redirect(url_for('latest'))
        return render_template('regist.html')
