from flask import render_template

from . import home
from ..auth.forms import LoginForm


@home.route('/')
def homepage():
    form = LoginForm()
    return render_template('index.html', form=form, title="Welcome")


@home.route('/about')
def about():
    return render_template('about.html', title="About")


@home.route('/teams')
def teams():
    return render_template('teams.html', title="Teams")


@home.route('/faq')
def faq():
    return render_template('faq.html', title="FAQ")
