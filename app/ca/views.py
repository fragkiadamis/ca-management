from flask import render_template, session, flash, redirect, url_for
from flask_login import login_required

from . import ca


@ca.route('/')
@login_required
def ca_home():
    return redirect(url_for('ca.dashboard'))


@ca.route('/dashboard')
@login_required
def dashboard():
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/dashboard.html', user=sess_user, title="Dashboard")
