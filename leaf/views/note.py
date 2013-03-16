#-*- coding:utf-8 -*-

from flask import render_template

from leaf import app
from leaf.models.note import Note
from leaf.models.user_model import User

@app.route('/notes')
def notes():
    users = User.query.all()
    user = users[0]
    notes = Note.gets_by_author(user.id)
    return render_template('note_list.html', notes=notes, user=user)

@app.route('/note/<int:note_id>')
def note(note_id):
    note = Note.get(note_id)
    return render_template('note.html', note=note)
