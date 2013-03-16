# -*- coding: utf-8 -*-

import hmac
from datetime import datetime, timedelta
from flask import (current_app, session, _request_ctx_stack, redirect, url_for,
                   request, flash, abort)
from flask.signals import Namespace
from functools import wraps
from hashlib import sha1, md5
from urlparse import urlparse, urlunparse
from werkzeug.local import LocalProxy
from werkzeug.urls import url_decode, url_encode

COOKIE_NAME = "remember_token"
COOKIE_DURATION = timedelta(days=365)

class LoginManager():

    def user_loader(self, callback):
        self.user_callback = callback

    def init_app(self, app):
        app.login_manager = self
        app.before_request(self._load_user)
        app.after_request(self._update_remember_cookie)
        app.context_processor(_user_context_processor)

    def _load_user(self):
        config = current_app.config
        cookie_name = config.get("REMEMBER_COOKIE_NAME",COOKIE_NAME)
        if cookie_name in request.cookies and 'user_id' not in session:
            self._load_from_cookie(request.cookies[cookie_name])
        else:
            self.reload_user()

    def _update_remember_cookie(self,response):
        operation = session.pop('remember',None)
        if operation == 'set' and 'user_id' in session:
            self._set_cookie(response)
        elif operation == 'clear':
            self._clear_cookie(response)
        return response

    def _set_cookie(self, response):
        config = current_app.config
        cookie_name = config.get('REMEMBER_COOKIE_NAME', COOKIE_NAME)
        duration = config.get('REMEMBER_COOKIE_DURATION', COOKIE_DURATION)

        data = encode_cookie(str(session['user_id']))
        expires = datatime.utcnow() + duration
        response.set_cookie(cookie_name,data,expires=expires)

    def _clear_cookie(self, response):
        config = current_app.config
        cookie_name = config.get('REMEMBER_COOKIE_NAME', COOKIE_NAME)
        response.delete_cookie(cookie_name)

    def _load_from_cookie(cookie):
        user_id = decode_cookie(cookie)
        if user_id is not None:
            session['user_id'] = user_id
            session['_fresh'] = False
        self.reload_user()

    def reload_user(self):
        ctx = _request_ctx_stack.top
        user_id = session.get('user_id',None)
        user = self.user_callback(user_id)
        if user_id is None:
            ctx.user = None
        else:
            ctx.user = user

def encode_cookie(cookie):
    return cookie

def decode_cookie(cookie):
    return cookie

def _get_user():
    return getattr(_request_ctx_stack.top, "user", None)

current_user = LocalProxy(lambda: _request_ctx_stack.top.user)

def _user_context_processor():
    return dict(current_user=_get_user())

def login_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if not current_user:
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return decorated_view

def login_user(user, remember=False):
    user_id = user.id
    session["user_id"] = user_id
    if remember:
        session["remember"] = "set"
    current_app.login_manager.reload_user()
    return True

def logout_user():
    if "user_id" in session:
        del session["user_id"]
    cookie_name = current_app.config.get("REMEMBER_COOKIE_NAME", COOKIE_NAME)
    if cookie_name in request.cookies:
        del session["remember"]
    current_app.login_manager.reload_user()
    return True

