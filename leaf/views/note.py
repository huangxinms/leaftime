#-*- coding:utf-8 -*-

from random import randint

from flask import render_template,request
from flask import json,jsonify

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
def latest():
    user_id = get_user_id()
    note = Note.query_obj.get_recent_note_by_user(user_id)
    note.time = note.time.strftime('%Y年%m月%d日').decode('utf-8')
    return render_template('note.html', note=note)

@app.route('/get_older_note/', methods=['GET'])
@login_required
def get_older_note():
    note_id = int(request.args.get('note_id'))
    user_id = get_user_id()
    note = Note.query_obj.get_older_note(user_id,note_id)
    note_id = note.id
    note_title = note.title
    note_content = note.content
    note_time = note.time.strftime('%Y年%m月%d日')
    return jsonify(
                id = note_id,
                title=note_title,
                time = note_time,
                content = note_content
            )

@app.route('/get_newer_note/', methods=['GET'])
@login_required
def get_newer_note():
    note_id = int(request.args.get('note_id'))
    user_id = get_user_id()
    note = Note.query_obj.get_newer_note(user_id,note_id)
    note_id = note.id
    note_title = note.title
    note_content = note.content
    note_time = note.time.strftime('%Y年%m月%d日')
    return jsonify(
                id = note_id,
                title=note_title,
                time = note_time,
                content = note_content
            )


@app.route('/get_random_note/', methods=['GET'])
@login_required
def get_random_note():
    note_id = int(request.args.get('note_id'))
    user_id = get_user_id()
    note_list = Note.query_obj.gets_by_author(user_id)
    note = note_list[randint(0, len(note_list)-1)]
    note_id = note.id
    note_title = note.title
    note_content = note.content
    note_time = note.time.strftime('%Y年%m月%d日')
    return jsonify(
                id = note_id,
                title=note_title,
                time = note_time,
                content = note_content
            )

@app.route('/write/',methods=['GET','POST'])
@login_required
def write():
    if request.method == 'GET':
        return render_template('write.html')
