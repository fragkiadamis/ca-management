from functools import update_wrapper
from flask import session, redirect, url_for, flash


def permissions_required(required_roles):
    def decorator(fn):
        def wrapped_function(*args, **kwargs):
            valid_role = [i for i in session['_user_roles'] if i in required_roles]
            if not valid_role:
                flash('You do not have the permission to do this')
                return redirect(url_for('ca.dashboard'))
            return fn(*args, **kwargs)
        return update_wrapper(wrapped_function, fn)
    return decorator
