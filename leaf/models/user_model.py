#-*- coding:utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
from leaf.extentions import db

class UserQuery:
    def get_by_username(self,username):
        user = User.query.filter_by(username=username).first()
        return user

    def get_by_email(self,email):
        user = User.query.filter_by(email=email).first()
        return user


class User(db.Model):
    query_obj = UserQuery()
    __tablename__ = 'user'
    id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    password = db.Column('password',db.VARCHAR(15),nullable=False)
    username = db.Column('username',db.VARCHAR(30),nullable=False,default='')
    email = db.Column('email',db.VARCHAR(63),nullable=False)
    create_time = db.Column('create_time',db.TIMESTAMP,nullable=False)
    status = db.Column('status',db.CHAR(1),nullable=False)

    @classmethod
    def create(password,username,email,created_time,status):
        user = User(password=password,username=username,email=email,created_time=created_time,       status=status)
        db.session.add(user)
        db.session.commit()
        return user

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def set_email(self,email):
        self.email = email
        db.session.commit()
