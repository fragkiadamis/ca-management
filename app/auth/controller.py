from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import validate_form
from .. import db
from ..models import Member


@auth.route('/register', methods=['GET', 'POST'])
@validate_form(form_type='register')
def register():
    if request.method == 'POST':
        if len(request.errors):
            return {'errors': request.errors}

        data = request.json
        member = Member(first_name=data['first_name'], last_name=data['last_name'], username=data['username'],
                        email=data['email'],
                        hashed_password=data['password'], telephone=data['telephone'], semester=data['semester'],
                        uni_reg_number=data['uni_reg_number'],
                        address=f"{data['city']}, {data['address']}")
        # add employee to the database
        db.session.add(member)
        db.session.commit()

        # redirect to the login page
        return {'redirect': url_for('public.homepage')}

    # load registration template
    return render_template('register.html', title='Register')


@auth.route('/login', methods=['POST'])
def login():
    print("Login")
    # form = LoginForm()
    # if form.validate_on_submit():
    #
    #     # check whether employee exists in the database and whether
    #     # the password entered matches the password in the database
    #     member = Member.query.filter_by(email=form.email.data).first()
    #     if member is not None and member.verify_password(
    #             form.password.data):
    #         # log employee in
    #         login_user(member)
    #
    #         # redirect to the dashboard page after login
    #         return redirect(url_for('public.dashboard'))
    #
    #     # when login details are incorrect
    #     else:
    #         flash('Invalid email or password.')


@auth.route('/logout')
@login_required
def logout():
    print("Logout")
    # logout_user()
    # flash('You have successfully been logged out.')
    #
    # # redirect to the login page
    # return redirect(url_for('index'))
