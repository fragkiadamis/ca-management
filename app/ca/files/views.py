from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from .forms import FileForm
from .. import ca
from app.models import File
from ... import db
from ...decorators import permissions_required


@ca.route('/dashboard/files', methods=['GET', 'POST'])
@login_required
def list_files():
    files = File.query.all()

    return render_template('private/dashboard.html',
                           member={'id': session['_user_id'], 'username': session['_username']},
                           files=files,
                           title="Dashboard")


@ca.route('/dashboard/files/<int:file_id>', methods=['GET', 'POST'])
@login_required
def get_file(file_id):
    file = File.query.get_or_404(file_id)

    return render_template('private/dashboard.html',
                           member={'id': session['_user_id'], 'username': session['_username']},
                           file=file)


@ca.route('/dashboard/files/add', methods=['GET', 'POST'])
@login_required
def add_file():
    # Add a file
    add_file = True

    form = FileForm()
    if form.validate_on_submit():
        file = File(name=form.name.data, path=form.path.data, type=form.type.data)
        # Add file to database
        db.session.add(file)
        db.session.commit()
        flash('You have successfully added a new file.')

        # redirect to dashboard
        return redirect(url_for('ca.list_files'))

    # Load Team template
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/file-actions.html',
                           action="Add", add_file=add_file, form=form,
                           user=sess_user,
                           title="Add File")


@ca.route('/dashboard/files/edit/<int:file_id>', methods=['GET', 'POST'])
@login_required
def edit_file(file_id):

    add_file = False

    file = File.query.get_or_404(file_id)
    form = FileForm(obj=file)
    if form.validate_on_submit():
        file.name = form.name.data
        file.path = form.path.data
        file.type = form.type.data
        db.session.commit()
        flash('You have successfully edited the file.')

        # Redirect to announcements page
        return redirect(url_for('ca.list_files'))

    form.name.data = file.name
    form.path.data = file.path
    form.type.data = file.type

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/file-actions.html', action="Edit",
                           add_file=add_file, form=form, file=file,
                           user=sess_user,
                           title="Edit File")


@ca.route('/dashboard/files/delete/<int:file_id>', methods=['GET', 'POST'])
@login_required
def delete_file(file_id):
    # Delete a specific file

    # check_admin()

    file = File.query.get_or_404(file_id)
    db.session.delete(file)
    db.session.commit()
    flash('You have successfully deleted the file.')

    # Redirect to the departments page
    return redirect(url_for('ca.list_files'))
