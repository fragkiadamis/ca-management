# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Member


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        member = Member(email=form.email.data, username=form.username.data)

        # add employee to the database
        db.session.add(member)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('register.html', form=form, title='Register')


@auth.route('/login', methods=['POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        member = Member.query.filter_by(email=form.email.data).first()
        if member is not None and member.verify_password(
                form.password.data):
            # log employee in
            login_user(member)

            # redirect to the dashboard page after login
            return redirect(url_for('public.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('index'))
