#-*- coding:utf-8 -*-
from flask import g,render_template

from leaf import app

@app.route('/hello',methods=['GET'])
def hello():
    return render_template('hello.html')
