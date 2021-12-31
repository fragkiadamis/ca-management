from flask import flash, redirect, render_template, url_for, session
from flask_login import login_user, login_required, logout_user

from . import auth
from .forms import RegistrationForm, LoginForm
from .. import db
from app.models import Member, Role


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        Member.insert_member(form)

        flash('You have successfully registered! You may now login.')
        # redirect to the login page
        return redirect(url_for('public.homepage'))

    # load registration template
    return render_template('register.html', form=form, title='Register')


@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        member = Member.verify_login(form)
        if member:
            login_user(member, form.remember_me.data)
            session['_username'] = member.username
            session['_user_roles'] = []
            for role in member.roles:
                session['_user_roles'].append(role.name)
            # redirect to the dashboard page after login
            return redirect(url_for('ca.dashboard'))
        else:
            flash('Invalid email or password.')
            return render_template('index.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_username')
    session.pop('_user_roles')
    # redirect to the homepage
    return redirect(url_for('public.homepage'))
