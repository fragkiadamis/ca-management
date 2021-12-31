from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from . import ca
from .forms import ProfileForm, TeamForm, ActivityForm, AnnouncementForm
from .. import db
from ..models import Member, Team, File, Activity, Announcement


@ca.route('/dashboard')
@login_required
def dashboard():
    return render_template('private/dashboard.html',
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title="Dashboard")


@ca.route('/dashboard/files', methods=['GET', 'POST'])
@login_required
def list_files():
    files = File.query.all()

    return render_template('private/dashboard.html',
                           member={'id': session['_user_id'], 'username': session['_username']},
                           files=files,
                           title="Dashboard")


@ca.route('/dashboard/files/add', methods=['GET', 'POST'])
@login_required
def add_file():
    # Add a file
    add_file = True

    # form = FileForm()
    # if form.validate_on_submit():
    #     file = File(name=form.name.data, path=form.path.data, type=form.type.data)
    #     # Add file to database
    #     db.session.add(file)
    #     db.session.commit()
    #     flash('You have successfully added a new file.')
    #
    #     # redirect to dashboard
    #     return redirect(url_for('ca.dashboard'))
    #
    # # Load Team template
    # return render_template('private/dashboard/add-file.html',
    #                        action="Add", add_file=add_file, form=form,
    #                        member={'id': session['_user_id'], 'username': session['_username']},
    #                        title="Add File")


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


@ca.route('/profile/<int:member_id>', methods=['GET', 'POST'])
@login_required
def profile(member_id):
    form = ProfileForm()
    member = Member.query.get_or_404(member_id)

    if form.validate_on_submit():
        if not member.verify_password(form.confirm_changes.data):
            flash('Invalid Password')
            return render_template('private/profile.html', form=form, member=member, title='Profile')

        if form.password.data:
            member.password = form.password.data

        # Update member properties
        member.first_name = form.first_name.data
        member.last_name = form.last_name.data
        member.username = form.username.data
        member.email = form.email.data
        member.telephone = form.telephone.data
        member.city = form.city.data
        member.address = form.address.data

        # Update database
        db.session.commit()

        flash('You have successfully updated your profile.')

    return render_template('private/profile.html', form=form, member=member, title='Profile')


@ca.route('/members', methods=['GET', 'POST'])
@login_required
def list_members():
    listing = request.args.get('list')
    members = {}

    # Filter Members according to url parameter
    if listing == 'Pending':
        members = {'Pending': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'Active':
        members = {'Active': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'Inactive':
        members = {'Inactive': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'Admin':
        members = {'Admin': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'CA Admin':
        members = {'CA Admin': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'Basic':
        members = {'Basic': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'role':
        all_members = Member.query.filter(Member.is_verified == 1)
        admins = [d for d in all_members if d.role == 'admin']
        ca_admins = [d for d in all_members if d.role == 'ca_admin']
        basics = [d for d in all_members if d.role == 'basic']
        members = {'Admins': admins, 'CA Admins': ca_admins, 'Basic': basics}
    else:
        members = {'Current': Member.query.filter(Member.is_verified == 1, Member.is_active == 1)}

    return render_template('private/members.html', member={'id': session['_user_id'], 'username': session['_username']},
                           members=members, title='Members')


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

