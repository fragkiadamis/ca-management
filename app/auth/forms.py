from functools import wraps
from flask import request
import re

from ..models import Member


def validate_form(form_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == 'POST':
                request.errors = []
                form_data = request.json
                # Check that all fields are filled
                for key in form_data:
                    if not form_data[key]:
                        request.errors.append({'field': key, 'msg': 'This field is required'})

                # Validate email
                email_pattern = re.compile("^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
                if not email_pattern.match(form_data['email']):
                    request.errors.append({'field': 'email', 'msg': 'Invalid email'})

                # Validate password and unique fields
                if form_type == 'register':
                    if not form_data['password'] == form_data['confirm_password']:
                        request.errors.append({'field': 'password', 'msg': 'The passwords do not match'})
                    if Member.query.filter_by(email=form_data['email']).first():
                        request.errors.append({'field': 'email', 'msg': 'Email already exists'})
                    if Member.query.filter_by(username=form_data['username']).first():
                        request.errors.append({'field': 'username', 'msg': 'Username already exists'})
                    if Member.query.filter_by(telephone=form_data['telephone']).first():
                        request.errors.append({'field': 'telephone', 'msg': 'Telephone already exists'})
                    if Member.query.filter_by(uni_reg_number=form_data['uni_reg_number']).first():
                        request.errors.append(
                            {'field': 'uni_reg_number', 'msg': 'University Registration Number already exists'})
            return func(*args, **kwargs)
        return wrapper
    return decorator
