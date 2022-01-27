from . import home

from flask import render_template

from app.auth.forms import LoginForm


@home.route('/')
def homepage():
    form = LoginForm()
    return render_template('index.html', form=form, title="Welcome")
