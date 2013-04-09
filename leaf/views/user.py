#-*- coding:utf-8 -*-

import random

from flask import render_template, request, redirect, flash, url_for

from leaf import app
from leaf.corelib.flask_login import login_user, logout_user, get_user_id
from leaf.corelib.mail import send_regist_mail
from leaf.models.user_model import User, UserRegist
from leaf.forms.user import LoginForm, RegistForm, RegistPasswordForm

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        user_id = get_user_id()
        if user_id:
            return redirect(url_for('latest'))
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        result = LoginForm(email=email, password=password).validate()
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
    return render_template('login.html', email=email)


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
    elif request.method == 'POST':
        email = request.form['email'].strip()
        result = RegistForm(email=email).validate()
        if result.is_success:
            code = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz',20))
            result = send_regist_mail(email,code)
            if result:
                user = User.query_obj.get_by_email(email)
                if user:
                    flash(u'该邮箱已经注册')
                else:
                    UserRegist.create(email, code)
                    return render_template('password.html',email=email)
            else:
                flash(u'邮箱无效，请重新填写')
        else:
            flash(result.message)
        return redirect(url_for('register'))

@app.route('/init-password',methods=['GET','POST'])
def init_password():
    if request.method == 'GET':
        return render_template('password.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = RegistPasswordForm(email=email, password=password)
        if result:
            user = User.create(email=email, password=password)
            login_user(user)
            return render_template('write.html')
        else:
            return render_templete('password.html')
