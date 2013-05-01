#-*- coding:utf-8 -*-

from datetime import datetime
import random

from leaf.extentions import db
from leaf.corelib import secure, cache, mc
from leaf.corelib.consts import USER_STATUS_INVALID, USER_STATUS_NORMAL, USER_STATUS_SUICIDE

class UserRegistQuery:

    def get_by_email(self,email):
        user = UserRegist.query.filter_by(email=email).order_by('-id').first()
        return user


class UserRegist(db.Model):
    query_obj = UserRegistQuery()
    __tablename__ = 'user_regist'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column('email', db.VARCHAR(63), nullable=False)
    code = db.Column('code', db.VARCHAR(150), nullable=False)
    create_time = db.Column('create_time', db.TIMESTAMP, nullable=False)

    @classmethod
    def create(cls, email, code):
        user = UserRegist(email=email, code=code, create_time=datetime.now())
        db.session.add(user)
        db.session.commit()

    def check(self, code):
        return self.code == code

    def set_status(self, status):
        self.status = status
        db.session.commit()

class UserQuery:

    def get_by_email(self, email):
        user = User.query.filter_by(email=email).first()
        return user

    @cache('user:get_by_id:{id}')
    def get_by_id(self, id=0):
        user = User.query.filter_by(id=id).first()
        return user


class User(db.Model):
    query_obj = UserQuery()
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    password = db.Column('password', db.VARCHAR(150), nullable=False)
    salt = db.Column('salt', db.VARCHAR(20), nullable=False)
    email = db.Column('email', db.VARCHAR(63), nullable=False)
    create_time = db.Column('create_time', db.TIMESTAMP, nullable=False)
    status = db.Column('status', db.CHAR(1), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @classmethod
    def create(cls, email, password, create_time=datetime.now(),
            status=USER_STATUS_NORMAL):
        salt,password = secure.encrypt(password)
        user = User(salt=salt, password=password, email=email,
                    create_time=create_time, status=status)
        db.session.add(user)
        db.session.commit()
        return user

    def check(self, password):
        return secure.check_user(password,self.salt,self.password)

    def set_email(self, email):
        self.email = email
        db.session.commit()
        self.__clear_cache()

    def set_status(self, status):
        self.status = status
        db.session.commit()
        self.__clear_cache()

    def set_password(self, password):
        salt,en_password = secure.encrypt(password)
        self.password = en_password
        self.salt = salt
        db.session.commit()
        self.__clear_cache()

    def __clear_cache(self):
        mc.delete('user:get_by_id:%s' %self.id)

