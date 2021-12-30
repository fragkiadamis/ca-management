from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from . import ca
from .forms import ProfileForm, TeamForm
from .. import db
from ..models import Member
from ..models import Team


@ca.route('/dashboard')
@login_required
def dashboard():
    return render_template('private/dashboard.html',
                           member={'id': session['_user_id'], 'username': session['_username']}, title="Dashboard")


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

    return render_template('private/teams.html',
                           teams=teams,
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title="Teams")


@ca.route('/teams/add', methods=['GET', 'POST'])
@login_required
def add_team():
    # Add a specific team
    add_team = True

    form = TeamForm()
    if form.validate_on_submit():
        team = Team(name=form.name.data, description=form.description.data, email=form.email.data, telephone=form.telephone.data)

        try:
            # Add team to database
            db.session.add(team)
            db.session.commit()
            flash('You have successfully added a new team.')
        except:
            # If team name already exists
            flash('Error: Team name already exists.')

        # redirect to teams page
        # return redirect(url_for('ca.list_teams'))

    # Load Team template
    return render_template('private/team.html',
                           action="Add", add_team=add_team, form=form,
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title="Add Team")


@ca.route('/teams/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team(id):
    # Edit a specific team
    add_team = False

    team = Team.query.get_or_404(id)
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        team.name = form.name.data
        team.description = form.description.data
        team.email = form.email.data
        team.telephone = form.telephone.data
        db.session.commit()
        flash('You have successfully edited the team.')

        # Redirect to teams page
        # return redirect(url_for('ca.list_teams'))

        form.description.data = team.description
        form.name.data = team.name
        form.email.data = team.email
        form.telephone.data = team.telephone

        return render_template('private/team.html', action="Edit",
                               add_team=add_team, form=form, team=team,
                               member={'id': session['_user_id'], 'username': session['_username']},
                               title="Edit Team")


@ca.route('/teams/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_team(id):
    # Delete a team with a specific id

    # check_admin()
    team = Team.query.get_or_404(id)
    db.session.delete(team)
    db.session.commit()
    flash('You have successfully delete the team.')

    # Redirect to the departments page
    # return redirect(url_for(ca.list_teams))

    return render_template('private/team.html', action="Edit", add_team=add_team, form=form, team=team,
                           member={'id': session['_user_id'], 'username': session['_username']},
                           title="Delete Team")

