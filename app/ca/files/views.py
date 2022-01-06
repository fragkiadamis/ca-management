import os

from flask import render_template, session, flash, redirect, url_for, send_from_directory
from flask_login import login_required
from werkzeug.utils import secure_filename

from .forms import FileForm
from .. import ca
from app.models import File, Team
from ... import db
from ...decorators import permissions_required


@ca.route('/files')
@login_required
def list_files():
    files = File.query.all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/files/files.html', user=sess_user, files=files, title="Files")


@ca.route('/files/add', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = FileForm()
    if form.validate_on_submit():
        file = form.file_field.data
        file_name = f'{secure_filename(file.filename)}'
        file_path = os.path.join(os.path.dirname(f'{os.path.dirname(__file__)}/../../static/files/'), file_name)
        file.save(file_path)
        file = File(name=form.name.data, file_name=file_name, added_by=session['_user_id'])
        for team_id in form.teams.data:
            file.teams.append(Team.query.get_or_404(team_id))
        db.session.add(file)
        db.session.commit()

        flash('You have successfully added a new file.')
        return redirect(url_for('ca.list_files'))

    # Load Team template
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/files/file_form.html', user=sess_user, form=form, title="Add File")


@ca.route('/files/download/<int:file_id>')
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    return send_from_directory(directory=os.path.dirname(f'{os.path.dirname(__file__)}/../../static/files/'), path=file.file_name)


@ca.route('/files/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    os.remove(os.path.join(os.path.dirname(f'{os.path.dirname(__file__)}/../../static/files/'), file.file_name))
    db.session.delete(file)
    db.session.commit()

    flash('You have successfully deleted the file.')
    return redirect(url_for('ca.list_files'))
