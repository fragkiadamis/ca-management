from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from .forms import TeamForm
from .. import ca
from ... import db
from ...decorators import permissions_required
from ...models import Team


@ca.route('/teams')
@login_required
def list_teams():
    teams = Team.query.all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/teams/teams.html', teams=teams, user=sess_user, title="Teams")


@ca.route('/teams/add', methods=['GET', 'POST'])
@login_required
def add_team():
    form = TeamForm()
    if form.validate_on_submit():
        team = Team(name=form.name.data, description=form.description.data, email=form.email.data, telephone=form.telephone.data)
        db.session.add(team)
        db.session.commit()

        flash('You have successfully added a new team.')
        return redirect(url_for('ca.list_teams'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/teams/team_form.html', user=sess_user, action='add', form=form, title="Add Team")


@ca.route('/teams/edit/<int:team_id>', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):
    form = TeamForm()
    team = Team.query.get_or_404(team_id)
    if form.validate_on_submit():
        team.name = form.name.data
        team.description = form.description.data
        team.email = form.email.data
        team.telephone = form.telephone.data
        db.session.commit()

        flash('You have successfully edited the team.')
        return redirect(url_for('ca.list_teams'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/teams/team_form.html', team=team, user=sess_user, action='edit', form=form, title="Edit Team")


@ca.route('/teams/delete/<int:team_id>')
@login_required
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()

    flash('You have successfully deleted the team.')
    return redirect(url_for('ca.list_teams'))
