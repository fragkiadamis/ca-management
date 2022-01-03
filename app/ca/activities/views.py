from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from .forms import ActivityForm
from .. import ca
from ... import db
from ...decorators import permissions_required
from ...models import Activity


@ca.route('/activities', methods=['GET', 'POST'])
@login_required
def list_activities():
    activities = Activity.query.all()

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/activities/activities.html',
                           user=sess_user,
                           activities=activities,
                           title="Activities")


@ca.route('/activities/activity/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def get_activity(activity_id):
    # Get a specific team
    activity = Activity.query.get_or_404(activity_id)
    print(activity.createDate)
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/activities/activity.html', activity=activity,
                           user=sess_user,
                           title=activity.title)


@ca.route('/activities/add', methods=['GET', 'POST'])
@login_required
def add_activity():
    # Add a activity
    add_activity = True

    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(title=form.title.data, description=form.description.data, activityDate=form.activityDate.data)
        # Add activity to database
        db.session.add(activity)
        db.session.commit()
        flash('You have successfully added a new activity.')

        # redirect to activities page
        return redirect(url_for('ca.list_activities'))

    # Load Activity template
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/activities/activity-actions.html',
                           action="Add", add_activity=add_activity, form=form,
                           user=sess_user,
                           title="Add Activity")


@ca.route('/activities/edit/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def edit_activity(activity_id):
    # Edit a specific activity
    add_activity = False

    activity = Activity.query.get_or_404(activity_id)
    form = ActivityForm(obj=activity)
    if form.validate_on_submit():
        activity.title = form.title.data
        activity.description = form.description.data
        activity.createDate = form.createDate.data
        activity.activityDate = form.activityDate.data
        db.session.commit()
        flash('You have successfully edited the activity.')

        # Redirect to activities page
        return redirect(url_for('ca.list_teams'))

    form.title.data = activity.title
    form.description.data = activity.description
    form.activityDate.data = activity.activityDate

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/activities/activity-actions.html', action="Edit",
                           add_activity=add_activity, form=form, activity=activity,
                           user=sess_user,
                           title="Edit Activity")


@ca.route('/activities/delete/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def delete_activity(activity_id):
    # Delete an activity with a specific id

    # check_admin()

    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()
    flash('You have successfully deleted the activity.')

    # Redirect to the departments page
    return redirect(url_for('ca.list_activities'))

    # return render_template(title="Delete Team")
