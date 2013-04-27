#-*- coding:utf-8 -*-

from random import randint
import datetime
import cgi
import new

from flask import render_template, request, redirect, url_for
from flask import jsonify
import json

from leaf import app
from leaf.models.note import Note
from leaf.corelib import format_textarea
from leaf.corelib.flask_login import get_user_id, login_required
from leaf.corelib.ext_date import get_local_weekday,get_local_date

@app.route('/notes/<datenum>')
@app.route('/notes/')
@login_required
def notes(datenum=None):
    user_id = get_user_id()
    if datenum is None:
        notes = Note.query_obj.get_notes_by_author(user_id)
        datenum = ''
    else:
        notes = Note.query_obj.get_notes_by_datenum(user_id,datenum)
    if not notes:
        return redirect(url_for('no_notes'))
    for note in notes:
        note.weekday = get_local_weekday(note.time)
        note.time = get_local_date(note.time)

    date_list = [str(d) for d, in Note.query_obj.get_datenum_by_user(user_id)]
    date_list = sorted(date_list,reverse=True)
    return render_template('note_list.html', notes=notes, date_list=date_list, datenum=datenum)

@app.route('/get_notes_by_date')
@login_required
def get_notes_by_date():
    user_id = get_user_id()
    datenum = int(request.args.get('datenum'))
    notes = Note.query_obj.get_notes_by_datenum(user_id,datenum)
    json_note_list = []
    for note in notes:
        note.weekday = get_local_weekday(note.time)
        note.time = get_local_date(note.time)
        json_note_list = json.dumps(new(note),cls=MyEncoder)
    return json.dumps(json_note_list)

@app.route('/latest')
@login_required
def latest():
    user_id = get_user_id()
    note = Note.query_obj.get_recent_note_by_user(user_id)
    if not note:
        return redirect(url_for('no_notes'))
    note.weekday = get_local_weekday(note.time)
    note.time = get_local_date(note.time)
    return render_template('note.html', note=note)


@app.route('/get_older_note', methods=['GET'])
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


@app.route('/get_newer_note', methods=['GET'])
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

# FIXME: 有可能获取到跟当前日记重复的日记，需过滤
@app.route('/get_random_note', methods=['GET'])
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
        note_content = format_textarea(note_content)
        try:
            note_date = datetime.datetime.strptime(note_date, '%Y-%m-%d')
        except ValueError:
            note_date = datetime.datetime.now()

        user_id = get_user_id()
        Note.create(user_id,  note_content, note_date)
        return redirect(url_for("notes"))

@app.route('/nonotes')
@login_required
def no_notes():
    return render_template('no_notes.html')
