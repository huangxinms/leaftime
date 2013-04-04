#-*- coding:utf-8 -*-

from random import randint
import datetime
import cgi

from flask import render_template, request, redirect, url_for
from flask import jsonify

from leaf import app
from leaf.models.note import Note
from leaf.corelib.flask_login import get_user_id, login_required
from leaf.corelib.ext_date import get_local_weekday,get_local_date

@app.route('/notes/')
def notes():
    user_id = get_user_id()
    notes = Note.query_obj.get_notes_by_author(user_id)
    for note in notes:
        note.weekday = get_local_weekday(note.time)
        note.time = get_local_date(note.time)
    return render_template('note_list.html', notes=notes)


@app.route('/latest')
@login_required
def latest():
    user_id = get_user_id()
    note = Note.query_obj.get_recent_note_by_user(user_id)
    note.weekday = get_local_weekday(note.time)
    note.time = get_local_date(note.time)
    return render_template('note.html', note=note)


# /get_older_note/ -> /get_older_note
@app.route('/get_older_note/', methods=['GET'])
@login_required
def get_older_note():
    note_id = int(request.args.get('note_id'))
    user_id = get_user_id()
    note = Note.query_obj.get_older_note(user_id,note_id)
    note_id = note.id
    note_content = note.content
    note_weekday = get_local_weekday(note.time)
    note_time = get_local_date(note.time)
    return jsonify(
                id = note_id,
                weekday = note_weekday,
                time = note_time,
                content = note_content
            )


# /get_newer_note/ -> /get_newer_note
@app.route('/get_newer_note/', methods=['GET'])
@login_required
def get_newer_note():
    note_id = int(request.args.get('note_id'))
    user_id = get_user_id()
    note = Note.query_obj.get_newer_note(user_id,note_id)
    note_id = note.id
    note_content = note.content
    note_weekday = get_local_weekday(note.time)
    note_time = get_local_date(note.time)
    return jsonify(
                id = note_id,
                weekday = note_weekday,
                time = note_time,
                content = note_content
            )

# /get_random_note/ -> /get_random_note
@app.route('/get_random_note/', methods=['GET'])
@login_required
def get_random_note():
    note_id = int(request.args.get('note_id'))
    user_id = get_user_id()
    note_list = Note.query_obj.get_notes_by_author(user_id)
    note = note_list[randint(0, len(note_list)-1)]
    note_id = note.id
    note_content = note.content
    note_weekday = get_local_weekday(note.time)
    note_time = get_local_date(note.time)
    return jsonify(
                id = note_id,
                weekday = note_weekday,
                time = note_time,
                content = note_content
            )

@app.route('/write',methods=['GET','POST'])
@login_required
def write():
    if request.method == 'GET':
        return render_template('write.html')
    elif request.method == 'POST':
        note_date = request.form["note_date"]
        note_content = request.form["note_content"]
        note_content = cgi.escape(note_content)
        try:
            note_date = datetime.datetime.strptime(note_date, '%Y/%m/%d')
        except ValueError:
            note_date = datetime.datetime.now()

        user_id = get_user_id()
        Note.create(user_id, 'NOTE DEFAULT TITLE', note_content, note_date)
        return redirect(url_for("notes"))
