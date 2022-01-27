from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required
from sqlalchemy import func

from .helpers import filter_members
from ...filters import filter_simple_view
from .. import ca
from .forms import ProfileForm, EditMemberForm
from app.models import Member, Roles, Team
from ... import db
from ...decorators import permissions_required, is_this_user


@ca.route('/members', methods=['GET', 'POST'])
@login_required
def list_members():
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}

    if 'Admin' in session['_user_roles'] or 'Admin Council' in session['_user_roles']:
        filter_by = request.args.get('filter_by')
        members, roles, teams, schools, departments = filter_members(filter_by)
        return render_template('private/members/members.html', user=sess_user, title='Members', members=members, teams=teams, schools=schools, departments=departments, roles=roles, filter_by=filter_by)
    else:
        members = filter_simple_view(session['_user_id'])
        return render_template('private/members/members.html', user=sess_user, title='Members', members=members)


@ca.route('/members/<int:member_id>', methods=['GET', 'POST'])
@login_required
@is_this_user
def profile(member_id):
    form = ProfileForm()
    member = Member.query.get_or_404(member_id)

    if form.validate_on_submit():
        if not member.verify_password(form.confirm_changes.data):
            flash('Invalid Password')
            return redirect(url_for('ca.profile', member_id=member_id))

        # Update member properties
        if form.password.data:
            member.password = form.password.data
        member.first_name = form.first_name.data
        member.last_name = form.last_name.data
        member.username = form.username.data
        member.email = form.email.data
        member.telephone = form.telephone.data
        member.city = form.city.data
        member.address = form.address.data
        db.session.commit()

        session['_username'] = member.username
        flash('You have successfully updated your profile.')

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/members/member_form.html', form=form, member=member, user=sess_user, title='Profile')


@ca.route('/members/edit/<int:member_id>', methods=['GET', 'POST'])
@login_required
@permissions_required(['Admin', 'Admin Council'])
def edit_member(member_id):
    form = EditMemberForm()
    member = Member.query.get_or_404(member_id)
    title = f'Profile: {member.first_name} {member.last_name}, {member.ca_reg_number}'

    if form.validate_on_submit():
        if not member.verify_password(form.confirm_changes.data):
            flash('Invalid Password')
            return redirect(url_for('ca.edit_member', member_id=member_id))

        if form.password.data:
            member.password = form.password.data
        member.first_name = form.first_name.data
        member.last_name = form.last_name.data
        member.username = form.username.data
        member.email = form.email.data
        member.telephone = form.telephone.data
        member.city = form.city.data
        member.address = form.address.data
        member.ca_reg_number = int(form.ca_reg_number.data)
        member.department_id = form.department.data
        member.roles = []
        for role_id in form.roles.data:
            member.roles.append(Roles.query.get_or_404(role_id))
        member.teams = []
        for team_id in form.teams.data:
            member.teams.append(Team.query.get_or_404(team_id))

        db.session.commit()

        # In case that a user is editing his own profile, update session
        if member.id == int(session['_user_id']):
            session['_username'] = member.username
            session['_user_roles'] = []
            for role in member.roles:
                session['_user_roles'].append(role.name)

        flash('You have successfully updated the member\'s profile.')
        return redirect(url_for('ca.list_members'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/members/member_form.html', form=form, member=member, user=sess_user, title=title)


@ca.route('/status/<int:member_id>')
@login_required
@permissions_required(['Admin', 'Admin Council'])
def toggle_status(member_id):
    filter_by = request.args.get('filter_by')
    member = Member.query.get_or_404(member_id)
    member.is_active = not member.is_active
    db.session.commit()

    return redirect(url_for('ca.list_members', filter_by=filter_by))


@ca.route('/verify/<int:member_id>')
@login_required
@permissions_required(['Admin', 'Admin Council'])
def verify(member_id):
    verify_member = request.args.get('verify')
    member = Member.query.get_or_404(member_id)
    if verify_member == 'Accept':
        # Get last verified member's ca reg number and increase it to one and assign to new verified member
        last_reg_number = db.session.query(func.max(Member.ca_reg_number)).first()[0]
        member.ca_reg_number = int(last_reg_number) + 1
        member.is_verified = member.is_active = 1
    else:
        # Remove Member from team and department
        department = member.department
        department.members.remove(member)
        teams = member.teams
        for team in teams:
            team.members.remove(member)
        db.session.delete(member)

    db.session.commit()

    return redirect(url_for('ca.list_members', filter_by='pending'))
