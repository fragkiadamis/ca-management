from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from .forms import ActivityForm
from .. import ca
from ... import db
from ...models import Activity, Team
from ...filters import filter_entities


@ca.route('/activities')
@login_required
def list_activities():
    filter_by = request.args.get('filter_by')
    activities = Activity.query.all()
    teams = Team.query.all()
    entities = filter_entities(filter_by, activities, teams)
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/activities/activities.html', user=sess_user, activities=entities, teams=teams, title="Activities")


@ca.route('/activity/<int:activity_id>')
@login_required
def get_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/activities/single_activity.html', user=sess_user, activity=activity, title="Dashboard")


@ca.route('/activities/add', methods=['GET', 'POST'])
@login_required
def add_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(title=form.title.data, body=form.body.data, start_date=form.start_date.data, end_date=form.end_date.data, added_by_id=session['_user_id'])
        for team_id in form.teams.data:
            activity.teams.append(Team.query.get_or_404(team_id))
        db.session.add(activity)
        db.session.commit()

        flash('You have successfully added a new activity.')
        return redirect(url_for('ca.list_activities'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/activities/activity_form.html', user=sess_user, action='add', form=form, title="Add Activity")


@ca.route('/activities/edit/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def edit_activity(activity_id):
    form = ActivityForm()
    activity = Activity.query.get_or_404(activity_id)
    if form.validate_on_submit():
        activity.title = form.title.data
        activity.body = form.body.data
        activity.start_date = form.start_date.data
        activity.end_date = form.end_date.data
        activity.teams = []
        for team_id in form.teams.data:
            activity.teams.append(Team.query.get_or_404(team_id))
        db.session.commit()

        flash('You have successfully edited the activity.')
        return redirect(url_for('ca.list_activities'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/activities/activity_form.html', user=sess_user, activity=activity, action='edit', form=form, title="Edit Activity")


@ca.route('/activities/delete/<int:activity_id>')
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()

    flash('You have successfully deleted the activity.')
    return redirect(url_for('ca.list_activities'))
