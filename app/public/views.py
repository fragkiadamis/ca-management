# app/public/controller.py

from flask import render_template

from . import home


@home.route('/')
def homepage():
    return render_template('index.html', title="Welcome")


@home.route('/about')
def about():
    return render_template('about.html', title="About")


@home.route('/teams')
def teams():
    return render_template('teams.html', title="Teams")


@home.route('/faq')
def faq():
    return render_template('faq.html', title="FAQ")
