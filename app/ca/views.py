from flask import render_template, session, flash, redirect, url_for, request
from flask_login import login_required

from . import ca
from ..filters import get_related_entities
from ..models import Activity, Announcement, Member


@ca.route('/')
@login_required
def ca_home():
    return redirect(url_for('ca.dashboard'))


@ca.route('/dashboard')
@login_required
def dashboard():
    filter_by = request.args.get('filter_by')
    member = Member.query.get_or_404(int(session['_user_id']))
    activities, *activity_related_teams = get_related_entities(filter_by, member, ('Admin', 'Editor'), 'activities')
    announcements, *announcement_related_teams = get_related_entities(filter_by, member, ('Admin', 'Editor'), 'announcements')

    # From second list keep only the teams that do not exist in the first list
    additional_teams = list(set(announcement_related_teams[0]) - set(activity_related_teams[0]))
    # Combine the lists
    teams = activity_related_teams[0] + additional_teams

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/dashboard.html', user=sess_user, activities=activities, announcements=announcements, teams=teams, title="Dashboard")
