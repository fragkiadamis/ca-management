from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from .. import ca
from .forms import UniEntityForm, EditDepartmentForm
from app.models import Department, School
from ... import db
from ...decorators import permissions_required


@ca.route('/schools')
@login_required
@permissions_required(['Admin'])
def list_schools():
    print(session['_user_roles'])
    schools = School.query.all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}

    return render_template('private/uni_entities/uni_entities.html', current_list='schools', route='ca.add_school',
                           uni_entities=schools, user=sess_user, title='Schools')


@ca.route('/schools/add', methods=['GET', 'POST'])
@login_required
@permissions_required(['Admin'])
def add_school():
    form = UniEntityForm()
    if form.validate_on_submit():
        school = School(name=form.name.data, description=form.description.data)
        db.session.add(school)
        db.session.commit()

        flash('You have successfully added a new school.')
        return redirect(url_for('ca.list_schools'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/uni_entities/uni_entity_form.html', user=sess_user, action='add', entity='school', form=form, title='Add School')


@ca.route('/schools/edit/<int:school_id>', methods=['GET', 'POST'])
@login_required
@permissions_required(['Admin'])
def edit_school(school_id):
    form = UniEntityForm()
    school = School.query.get_or_404(school_id)
    if form.validate_on_submit():
        school.name = form.name.data
        school.description = form.description.data
        db.session.commit()

        flash('You have successfully edited the school.')
        return redirect(url_for('ca.list_schools'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/uni_entities/uni_entity_form.html', user=sess_user, action='edit', entity='school', school=school, form=form, title='Edit School')


@ca.route('/schools/delete/<int:school_id>')
@login_required
@permissions_required(['Admin'])
def delete_school(school_id):
    school = School.query.get_or_404(school_id)
    if school.member_count:
        flash('Cannot delete as there are members associated with this school')
    else:
        db.session.delete(school)
        db.session.commit()
        flash('You have successfully deleted the school.')

    return redirect(url_for('ca.list_schools'))


@ca.route('/schools/<int:school_id>/departments')
@login_required
@permissions_required(['Admin'])
def list_departments(school_id):
    departments = Department.query.filter_by(school_id=school_id).all()
    school = School.query.get_or_404(school_id)
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/uni_entities/uni_entities.html', uni_entities=departments, current_list="departments", route='ca.add_department', school=school, user=sess_user, title='Departments')


@ca.route('/schools/<int:school_id>/departments/add', methods=['GET', 'POST'])
@login_required
@permissions_required(['Admin'])
def add_department(school_id):
    form = UniEntityForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.description.data, school_id=school_id)
        db.session.add(department)
        db.session.commit()

        flash('You have successfully added a new school.')
        return redirect(url_for('ca.list_departments', school_id=school_id))

    school = School.query.get_or_404(school_id)
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/uni_entities/uni_entity_form.html', user=sess_user, action='add', entity='Department', school=school, form=form, title='Add Department')


@ca.route('/schools/<int:school_id>/departments/edit/<int:department_id>', methods=['GET', 'POST'])
@login_required
@permissions_required(['Admin'])
def edit_department(school_id, department_id):
    form = EditDepartmentForm()
    department = Department.query.get_or_404(department_id)
    school = School.query.get_or_404(school_id)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        department.school_id = form.schools.data
        db.session.commit()

        flash('You have successfully edited the school.')
        return redirect(url_for('ca.list_departments', school_id=school.id, department_id=department.id))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/uni_entities/uni_entity_form.html', user=sess_user, action='edit', entity='department', department=department, school=school, form=form, title='Edit Department')


@ca.route('/schools/<int:school_id>/departments/delete/<int:department_id>')
@login_required
@permissions_required(['Admin'])
def delete_department(school_id, department_id):
    department = Department.query.get_or_404(department_id)
    if department.member_count:
        flash('Cannot delete as there are members associated with this department')
    else:
        db.session.delete(department)
        db.session.commit()
        flash('You have successfully deleted the school.')

    return redirect(url_for('ca.list_departments', school_id=school_id))
