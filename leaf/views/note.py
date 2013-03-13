#-*- coding:utf-8 -*-

import datetime

from flask import render_template

from leaf import app
from leaf.models.note import Note
from leaf.models.user_model import User

@app.route('/notes',methods=['GET'])
def notes():
    users = User.query.all()
    if not users:
        user = User.create('111111', 'liaofeng', 'liaofeng.pro@gmail.com', datetime.datetime.now(), '')
    else:
        user = users[0]
    notes = Note.query.all()
    if not notes:
        Note.create(user.id, "what a nice day", "coding and coding, 18 until die!")
        Note.create(user.id, "how time flies", "从一个学校一个班，毕业已经三年了")
    notes = Note.gets_by_author(user.id)
    return render_template('note_list.html', notes=notes)
