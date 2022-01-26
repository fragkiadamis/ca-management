from flask import render_template, session, flash, redirect, url_for
from flask_login import login_required

from . import ca
from ..models import Activity, Announcement


@ca.route('/')
@login_required
def ca_home():
    return redirect(url_for('ca.dashboard'))


@ca.route('/dashboard')
@login_required
def dashboard():
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    activities = Activity.query.all()
    announcements = Announcement.query.all()
    return render_template('private/dashboard.html', user=sess_user, activities=activities, announcements=announcements,
                           title="Dashboard")
