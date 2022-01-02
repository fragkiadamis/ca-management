from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from .. import ca
from .forms import UniEntityForm
from app.models import Department, Institution, School
from ... import db
from ...decorators import permissions_required


@ca.route('/institutions', methods=['GET', 'POST'])
@login_required
# @permissions_required('Admin')
def institutions():
    form = UniEntityForm()
    if form.validate_on_submit():
        institution = Institution(name=form.name.data, abbreviation=form.abbreviation.data)
        db.session.add(institution)
        db.session.commit()

    institutions = Institution.query.all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/institutions.html', institutions=institutions, form=form, user=sess_user, title='Institutions')


@ca.route('/institutions/<int:institution_id>', methods=['GET', 'POST'])
@login_required
# @permissions_required('Admin')
def schools(institution_id):
    form = UniEntityForm()
    if form.validate_on_submit():
        school = School(name=form.name.data, abbreviation=form.abbreviation.data, institution_id=institution_id)
        db.session.add(school)
        db.session.commit()

    schools = School.query.filter_by(institution_id=institution_id).all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/schools.html', schools=schools, institution_id=institution_id, form=form, user=sess_user, title='Schools')


@ca.route('/schools/<int:school_id>', methods=['GET', 'POST'])
@login_required
# @permissions_required('Admin')
def departments(school_id):
    form = UniEntityForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data, abbreviation=form.abbreviation.data, school_id=school_id)
        db.session.add(department)
        db.session.commit()

    departments = Department.query.filter_by(school_id=school_id).all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/departments.html', departments=departments, school_id=school_id, form=form, user=sess_user, title='Departments')
