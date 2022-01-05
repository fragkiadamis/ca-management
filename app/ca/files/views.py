import os

from flask import render_template, session, flash, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from .forms import FileForm
from .. import ca
from app.models import File, Team
from ... import db
from ...decorators import permissions_required


@ca.route('/dashboard/files')
@login_required
def list_files():
    files = File.query.all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/files/files.html', user=sess_user, files=files, title="Files")


@ca.route('/dashboard/files/add', methods=['GET', 'POST'])
@login_required
def add_file():
    form = FileForm()
    if form.validate_on_submit():
        file = form.file_field.data
        name = secure_filename(file.filename)
        file.save(os.path.join('./app/static/files', name))

        flash('You have successfully added a new file.')
        return redirect(url_for('ca.list_files'))

    # Load Team template
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/files/file_form.html', user=sess_user, form=form, title="Add File")


@ca.route('/dashboard/files/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    # os.remove(os.path.join('./app/static/files', item.filename))

    flash('You have successfully deleted the file.')
    return redirect(url_for('ca.list_files'))
