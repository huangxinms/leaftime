#-*- coding:utf-8 -*-

from flask import render_template

from leaf import app
from leaf.models.note import Note
from leaf.corelib.flask_login import get_user_id,login_required

@app.route('/notes')
def notes():
    user_id = get_user_id()
    notes = Note.query_obj.get_recent_note_by_user(user_id)
    return render_template('note_list.html', notes=notes, user=user_id)

@app.route('/latest/')
@login_required
def note():
    user_id = get_user_id()
    note = Note.query_obj.get_recent_note_by_user(user_id)
    return render_template('note.html', note=note)
