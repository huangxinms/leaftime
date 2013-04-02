#-*- coding:utf-8 -*-

from datetime import datetime

from leaf.extentions import db

USER_STATUS_NORMAL = ''
USER_STATUS_SUICIDE = 's'

class UserQuery:

    def get_by_username(self, username):
        user = User.query.filter_by(username=username).first()
        return user

    def get_by_email(self, email):
        user = User.query.filter_by(email=email).first()
        return user

    def get_by_id(self, id):
        user = User.query.filter_by(id=id).first()
        return user


class User(db.Model):
    query_obj = UserQuery()
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    password = db.Column('password', db.VARCHAR(15), nullable=False)
    username = db.Column('username', db.VARCHAR(30), nullable=False, default='')
    email = db.Column('email', db.VARCHAR(63), nullable=False)
    create_time = db.Column('create_time', db.TIMESTAMP, nullable=False)
    status = db.Column('status', db.CHAR(1), nullable=False)

    def __repr__(self):
        return '<User %s, %s(%s)>' % (self.id, self.username, self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @classmethod
    def create(cls, username, password, email, create_time=datetime.now(),
            status=USER_STATUS_NORMAL):
        user = User(password=password, username=username, email=email,
                    create_time=create_time, status=status)
        db.session.add(user)
        db.session.commit()
        return user

    def set_email(self, email):
        self.email = email
        db.session.commit()

    def set_status(self, status):
        self.status = status
        db.session.commit()

    def check(self, password):
        # TODO: 改为MD5加密
        return self.password == password
