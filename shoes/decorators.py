from functools import wraps
from flask import abort
from flask_login import current_user

def super_admin_required(f):
    @wraps(f)
    def decorated_function():
        if current_user.role != 0:
            abort(403)
        return f()
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role == 2:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
