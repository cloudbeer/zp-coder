# -*- coding: utf-8 -*-
from functools import wraps
import random
import string
import hashlib
import json
import urllib
from flask import session, request, redirect
from models.orm import User
from models.project import project
from zp_web import get_db


__author__ = 'cloudbeer'


def rdm_code(size=8, chars=string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for x in range(size))


def salt():
    return rdm_code(size=16)


def challenge_code():
    return rdm_code(size=6, chars=string.digits)


def hash_pwd(pwd, salt):
    hs = hashlib.sha256(salt + pwd)
    return hs.hexdigest()


def is_name(s):
    is_ascii = all(ord(c) < 128 for c in s)
    is_ascii_first = not s[0].isdigit()
    is_contains_blank = not ' ' in s
    return is_ascii and is_ascii_first and is_contains_blank


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def str2val(string, default=None):
    """
    将字符串变成值
    :param string:
    :param default:
    :return:
    """
    for atom in (True, False, None):
        if str(atom) == string:
            return atom
    else:
        try:
            return int(string)
        except ValueError:
            if default is not None:
                return default
            try:
                return float(string)
            except ValueError:
                if default is not None:
                    return default
                return string


class json_res(dict):
    def __init__(self, state=False, message=None, **kwargs):
        super(json_res, self).__init__(**kwargs)
        self.state = state
        if message is not None:
            self.message = message

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            return None

    def __setattr__(self, name, value):
        self[name] = value

    def str(self):
        return json.dumps(self)


def s_user():
    """
    Get the user in session

    :return:
    """
    if 'user' in session:
        return session['user']
    elif 'email' in request.cookies and 'emailtoken' in request.cookies:
        email = request.cookies['email']
        emailtoken = request.cookies['emailtoken']
        if email is not None and emailtoken is not None:
            db = get_db()
            m_user = db.query(User).filter(User.email == email).first()
            if m_user is not None and hash_pwd(email, m_user.salt) == emailtoken:
                session['user'] = m_user
                return m_user
    return None


def s_project():
    if 'project' in session and session['project'] is not None:
        return session['project']
    else:
        m_project = project()
        session['project'] = m_project
        return m_project


def login_required_ajax(func):
    @wraps(func)
    def warpper_ajax(*args, **kwargs):
        user = s_user()
        if not user:
            return json_res(False, message='You must login first.').str()
        else:
            return func(*args, **kwargs)

    return warpper_ajax


def login_required(func):
    @wraps(func)
    def warpper_mormal(*args, **kwargs):
        user = s_user()
        if not user:
            return redirect('/account/login/?' + urllib.urlencode({'back': request.path}))
        else:
            return func(*args, **kwargs)

    return warpper_mormal
