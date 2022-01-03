from flask import render_template, session, flash
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
    return render_template('private/file-actions.html',
                           action="Add", add_file=add_file, form=form,
                           member={'id': session['_user_id'], 'username': session['_username']},
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

    return render_template('private/file-actions.html', action="Edit",
                           add_file=add_file, form=form, file=file,
                           member={'id': session['_user_id'], 'username': session['_username']},
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


@ca.route('/teams', methods=['GET', 'POST'])
@login_required
def list_teams():
    # List all teams
    teams = Team.query.all()

    return render_template('private/teams/teams.html',
                           teams=teams,
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title="Teams")


@ca.route('/teams/team/<int:team_id>', methods=['GET', 'POST'])
@login_required
def get_team(team_id):
    # Get a specific team
    team = Team.query.get_or_404(team_id)

    return render_template('private/teams/team.html', team=team,
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title=team.name)


@ca.route('/teams/add', methods=['GET', 'POST'])
@login_required
def add_team():
    # Add a team
    add_team = True

    form = TeamForm()
    if form.validate_on_submit():
        team = Team(name=form.name.data, description=form.description.data, email=form.email.data,
                    telephone=form.telephone.data)
        # Add team to database
        db.session.add(team)
        db.session.commit()
        flash('You have successfully added a new team.')

        # redirect to teams page
        return redirect(url_for('ca.list_teams'))

    # Load Team template
    return render_template('private/teams/team-actions.html',
                           action="Add", add_team=add_team, form=form,
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title="Add Team")


@ca.route('/teams/edit/<int:team_id>', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):
    # Edit a specific team
    add_team = False

    team = Team.query.get_or_404(team_id)
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        team.name = form.name.data
        team.description = form.description.data
        team.email = form.email.data
        team.telephone = form.telephone.data
        db.session.commit()
        flash('You have successfully edited the team.')

        # Redirect to teams page
        return redirect(url_for('ca.list_teams'))

    form.name.data = team.name
    form.description.data = team.description
    form.email.data = team.email
    form.telephone.data = team.telephone

    return render_template('private/teams/team-actions.html', action="Edit",
                           add_team=add_team, form=form, team=team,
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title="Edit Team")


@ca.route('/teams/delete/<int:team_id>', methods=['GET', 'POST'])
@login_required
def delete_team(team_id):
    # Delete a team with a specific id

    # check_admin()

    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    flash('You have successfully deleted the team.')

    # Redirect to the departments page
    return redirect(url_for('ca.list_teams'))

    # return render_template(title="Delete Team")


@ca.route('/activities', methods=['GET', 'POST'])
@login_required
def list_activities():
    activities = Activity.query.all()

    return render_template('private/activities/activities.html',
                           member={'id': session['_user_id'], 'username': session['_username']},
                           activities=activities,
                           title="Activities")


@ca.route('/activities/activity/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def get_activity(activity_id):
    # Get a specific team
    activity = Activity.query.get_or_404(activity_id)

    return render_template('private/activities/activity.html', activity=activity,
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title=activity.title)


@ca.route('/activities/add', methods=['GET', 'POST'])
@login_required
def add_activity():
    # Add a activity
    add_activity = True

    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(title=form.title.data, description=form.description.data,
                            createDate=form.createDate.data, activityDate=form.activityDate.data)
        # Add activity to database
        db.session.add(activity)
        db.session.commit()
        flash('You have successfully added a new activity.')

        # redirect to activities page
        return redirect(url_for('ca.list_activities'))

    # Load Activity template
    return render_template('private/activities/activity-actions.html',
                           action="Add", add_activity=add_activity, form=form,
                           member={'id': session['_user_id'], 'username': session['_username']},
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
    form.createDate.data = activity.createDate
    form.activityDate.data = activity.activityDate

    return render_template('private/activities/activity-actions.html', action="Edit",
                           add_activity=add_activity, form=form, activity=activity,
                           member={'id': session['_user_id'], 'username': session['_username']},
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


@ca.route('/dashboard/announcements', methods=['GET', 'POST'])
@login_required
def list_announcements():
    announcements = Announcement.query.all()

    return render_template('private/dashboard.html',
                           member={'id': session['_user_id'], 'username': session['_username']},
                           announcements=announcements,
                           title="Dashboard")


@ca.route('/dashboard/announcements/<int:announcement_id>', methods=['GET', 'POST'])
@login_required
def get_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)

    return render_template('private/dashboard.html',
                           member={'id': session['_user_id'], 'username': session['_username']},
                           announcement=announcement,
                           title="Dashboard")


@ca.route('/dashboard/announcements/add', methods=['GET', 'POST'])
@login_required
def add_announcement():
    # Add an announcement
    add_announcement = True

    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, description=form.description.data, createDate=form.createDate.data)
        # Add announcement to database
        db.session.add(announcement)
        db.session.commit()
        flash('You have successfully added a new announcement.')

        # redirect to dashboard
        return redirect(url_for('ca.dashboard'))

    # Load Team template
    return render_template('private/announcement-actions.html',
                           action="Add", add_announcement=add_announcement, form=form,
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title="Add Announcement")


@ca.route('/dashboard/announcements/edit/<int:announcement_id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(announcement_id):
    # Edit a specific announcement
    add_announcement = False

    announcement = Announcement.query.get_or_404(announcement_id)
    form = AnnouncementForm(obj=announcement)
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.description = form.description.data
        announcement.createDate = form.createDate.data
        db.session.commit()
        flash('You have successfully edited the announcement.')

        # Redirect to announcements page
        return redirect(url_for('ca.list_announcements'))

    form.title.data = announcement.title
    form.description.data = announcement.description
    form.createDate.data = announcement.createDate

    return render_template('private/announcement-actions.html', action="Edit",
                           add_announcement=add_announcement, form=form, announcement=announcement,
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title="Edit Announcement")


@ca.route('/dashboard/announcements/delete/<int:announcement_id>', methods=['GET', 'POST'])
@login_required
def delete_announcement(announcement_id):
    # Delete a specific announcement

    # check_admin()

    announcement = Announcement.query.get_or_404(announcement_id)
    db.session.delete(announcement)
    db.session.commit()
    flash('You have successfully deleted the announcement.')

    # Redirect to the announcements page
    return redirect(url_for('ca.list_announcements'))

    # return render_template(title="Delete Team")
