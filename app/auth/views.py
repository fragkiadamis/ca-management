from flask import flash, redirect, render_template, url_for, session
from flask_login import login_user, login_required, logout_user

from . import auth
from .forms import RegistrationForm, LoginForm
from .. import db
from ..models import Member


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        member_exists = db.session.query(Member).first()

        ca_number = None
        role = None
        is_active = 0
        is_verified = 0
        if not member_exists:
            ca_number = 'ca1'
            role = 'admin'
            is_active = 1
            is_verified = 1

        member = Member(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            telephone=form.telephone.data,
            semester=form.semester.data,
            uni_reg_number=form.uni_reg_number.data,
            city=form.city.data,
            address=form.address.data,
            ca_reg_number = ca_number,
            role = role,
            is_active = is_active,
            is_verified = is_verified
        )

        db.session.add(member)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('public.homepage'))

        # load registration template
    return render_template('register.html', form=form, title='Register')


@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # check whether member exists in the database and whether
        # the password entered matches the password in the database
        member = Member.query.filter_by(email=form.email.data).first()
        if member is not None and member.is_verified and member.is_active and member.verify_password(form.password.data):
            # log employee in
            login_user(member, form.remember_me.data)
            session['_username'] = member.username
            session['_user_role'] = member.role

            # redirect to the dashboard page after login
            return redirect(url_for('ca.dashboard'))

        # when login details are incorrect
        elif not member.is_verified:
            flash('Your verification is pending')
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('index.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_username')
    session.pop('_user_role')
    # redirect to the homepage
    return redirect(url_for('public.homepage'))
