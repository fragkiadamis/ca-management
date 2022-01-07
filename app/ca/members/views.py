from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from .. import ca
from .forms import ProfileForm, EditMemberForm
from app.models import Member, Roles, MemberRoles, Team
from ... import db
from ...decorators import permissions_required, is_this_user


@ca.route('/members', methods=['GET', 'POST'])
@login_required
def list_members():
    display = request.args.get('display')
    members = None

    # Filter Members according to url parameter
    # TODO implement filters for basic users
    if display == 'pending':
        members = {'Pending': Member.query.filter(Member.is_verified == 0).all()}
    elif display == 'active':
        members = {'Active': Member.query.filter(Member.is_active == 1, Member.is_verified == 1).all()}
    elif display == 'inactive':
        members = {'Inactive': Member.query.filter(Member.is_active == 0, Member.is_verified == 1).all()}
    elif display == 'admin':
        members = {'Admin': Member.query.filter(Member.role == 'admin', Member.is_verified == 1).all()}
    elif display == 'ca_admin':
        members = {'CA Admin': Member.query.filter(Member.role == 'ca_admin', Member.is_verified == 1).all()}
    elif display == 'basic':
        members = {'Basic': Member.query.filter(Member.role == 'basic', Member.is_verified == 1).all()}
    elif display == 'role':
        all_members = Member.query.filter(Member.is_verified == 1).all()
        # admins = [d for d in all_members if d.roles == 'Admin']
        # ca_admins = [d for d in all_members if d.roles == 'Admin Council']
        # basics = [d for d in all_members if d.roles == 'Editor']
        # members = {'Admins': admins, 'CA Admins': ca_admins, 'Treasurer': basics}
    elif display == 'status':
        all_members = Member.query.filter(Member.is_verified == 1).all()
        active = [d for d in all_members if d.is_active]
        inactive = [d for d in all_members if not d.is_active]
        members = {'Active': active, 'Inactive': inactive}
    else:
        members = {'Current': Member.query.filter(Member.is_verified == 1, Member.is_active == 1).all()}

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/members/members.html', user=sess_user, members=members, title='Members', display=display)


@ca.route('/members/<int:member_id>', methods=['GET', 'POST'])
@login_required
@is_this_user
def profile(member_id):
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}

    form = ProfileForm()
    member = Member.query.get_or_404(member_id)

    if form.validate_on_submit():
        if not member.verify_password(form.confirm_changes.data):
            flash('Invalid Password')
            return render_template('private/members/member_form.html', form=form, user=sess_user, title='Profile')

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
        flash('You have successfully updated your profile.')

    return render_template('private/members/member_form.html', form=form, member=member, user=sess_user, title='Profile')


@ca.route('/members/edit/<int:member_id>', methods=['GET', 'POST'])
@login_required
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
        member.ca_reg_number = form.ca_reg_number.data
        member.department = form.department.data
        member.roles = []
        for role_id in form.roles.data:
            member.roles.append(Roles.query.get_or_404(role_id))
        member.teams = []
        for team_id in form.teams.data:
            member.teams.append(Team.query.get_or_404(team_id))

        db.session.commit()
        flash('You have successfully updated the member\'s profile.')
        return redirect(url_for('ca.list_members'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/members/member_form.html', form=form, member=member, user=sess_user, title=title)


@ca.route('/status/<int:member_id>')
@login_required
# @permissions_required(['Admin', 'CA Admin'])
def toggle_status(member_id):
    display = request.args.get('display')
    member = Member.query.get_or_404(member_id)
    member.is_active = not member.is_active
    db.session.commit()

    return redirect(url_for('ca.list_members', display=display))


@ca.route('/verify/<int:member_id>')
@login_required
# @permissions_required(['Admin', 'CA Admin'])
def verify(member_id):
    verify_member = request.args.get('verify')
    member = Member.query.get_or_404(member_id)
    if verify_member == 'Accept':
        # Get last verified member's ca reg number and increase it to one and assign to new verified member
        last_member = Member.query.filter(Member.is_verified == 1).order_by(Member.id.desc()).first()
        incremental = int(''.join(x for x in last_member.ca_reg_number if x.isdigit())) + 1
        member.ca_reg_number = f'ca{incremental}'
        member.is_verified = member.is_active = 1
        db.session.commit()
    else:
        db.session.delete(member)
        db.session.commit()

    return redirect(url_for('ca.list_members', display='pending'))