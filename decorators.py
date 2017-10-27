#encoding: utf-8

#获取装饰器函数
from functools import wraps
from flask import session,redirect,url_for

#写一个登录限制装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper
