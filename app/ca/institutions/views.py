from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from .. import ca
from .forms import UniversityEntityForm
from app.models import Department, School
from ... import db
from ...decorators import permissions_required


@ca.route('/schools')
@login_required
# @permissions_required('Admin')
def list_schools():
    form = UniversityEntityForm()
    schools = School.query.all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/schools.html', department_list='ca.list_departments', add_entity='ca.add_school', uni_entities=schools, form=form, user=sess_user, title='Schools')


@ca.route('/schools/add', methods=['POST'])
@login_required
# @permissions_required('Admin')
def add_school():
    form = UniversityEntityForm()
    if form.validate_on_submit():
        school = School(name=form.name.data, description=form.description.data)
        db.session.add(school)
        db.session.commit()

    return redirect(url_for('ca.list_schools'))


@ca.route('/schools/<int:school_id>/departments')
@login_required
# @permissions_required('Admin')
def list_departments(school_id):
    form = UniversityEntityForm()
    departments = Department.query.filter_by(school_id=school_id).all()
    school = School.query.filter_by(id=school_id).first()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/schools.html', uni_entities=departments, add_entity='ca.add_department', school=school, form=form, user=sess_user, title='Departments')


@ca.route('/schools/<int:school_id>/departments', methods=['POST'])
@login_required
# @permissions_required('Admin')
def add_department(school_id):
    form = UniversityEntityForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data, school_id=school_id)
        db.session.add(department)
        db.session.commit()

    return redirect(url_for('ca.list_departments', school_id=school_id))
