from flask import flash, redirect, render_template, url_for, session
from flask_login import login_user, login_required, logout_user

from . import auth
from .forms import RegistrationForm, LoginForm
from .. import db
from app.models import Member, Roles, Team


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        member = Member(
            first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data,
            department=form.department.data, email=form.email.data, password=form.password.data,
            telephone=form.telephone.data, uni_reg_number=form.uni_reg_number.data,
            city=form.city.data, address=form.address.data
        )
        for team_id in form.teams.data:
            member.teams.append(Team.query.get_or_404(team_id))
        db.session.add(member)
        db.session.commit()

        flash('You have successfully registered! You may now login.')
        return redirect(url_for('public.homepage'))

    # load registration template
    return render_template('register.html', form=form, title='Register')


@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        member = Member.query.filter_by(email=form.email.data).first()
        if member and member.verify_password(form.password.data) and member.is_verified and member.is_active:
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
