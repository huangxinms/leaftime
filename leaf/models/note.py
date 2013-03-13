# -*- coding: utf-8 -*-

import datetime

from leaf.extentions import db

class Note(db.Model):

    __tablename__ = 'note'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    # TODO: add index on `user_id`
    user_id = db.Column('user_id', db.Integer, nullable=False)
    title = db.Column('title', db.VARCHAR(255), nullable=False)
    time = db.Column('time', db.TIMESTAMP, nullable=False)
    update_time = db.Column('update_time', db.TIMESTAMP, nullable=True)
    content = db.Column('content', db.Text, nullable=False)
    
    def __init__(self, user_id, title, content, time, update_time): 
        self.user_id = user_id
        self.title = title
        self.time = time
        self.update_time = update_time
        self.content = content

    def __repr__(self):
        return "<Note id=%s, author_id=%s>" % (self.id, self.user_id)

    @classmethod
    def create(cls, user_id, title, content, time, update_time):
        note = cls(user_id, title, content, time, update_time)
        db.session.add(note)
        db.session.commit()
        return note

    def update(self, title, content):
        self.title = title
        self.content = content
        self.update_time = datetime.datetime.now()
        db.session.commit()
    
    @classmethod
    def gets_by_author(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get(cls, id):
        return cls.query.get(id)
