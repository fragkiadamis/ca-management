from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from .forms import TeamForm
from .. import ca
from ... import db
from ...decorators import permissions_required
from ...models import Team


@ca.route('/teams', methods=['GET', 'POST'])
@login_required
def list_teams():
    # List all teams
    teams = Team.query.all()

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/teams/teams.html',
                           teams=teams,
                           user=sess_user,
                           title="Teams")


@ca.route('/teams/team/<int:team_id>', methods=['GET', 'POST'])
@login_required
def get_team(team_id):
    # Get a specific team
    team = Team.query.get_or_404(team_id)

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/teams/team.html', team=team,
                           user=sess_user,
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
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/teams/team-actions.html',
                           action="Add", add_team=add_team, form=form,
                           user=sess_user,
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

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/teams/team-actions.html', action="Edit",
                           add_team=add_team, form=form, team=team,
                           user=sess_user,
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
