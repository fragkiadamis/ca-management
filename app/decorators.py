from functools import update_wrapper
from flask import session, redirect, url_for, flash, request

def is_this_user(fn):
    def wrapped_function(member_id, *args, **kwargs):
        if not (int(member_id) == int(session['_user_id'])):
            return redirect(url_for('ca.dashboard'))
        return fn(member_id, *args, **kwargs)
    return update_wrapper(wrapped_function, fn)


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
