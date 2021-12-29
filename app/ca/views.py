from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from . import ca
from .forms import ProfileForm
from .. import db
from ..models import Member


@ca.route('/')
@login_required
def ca_home():
    return redirect(url_for('ca.dashboard'))


@ca.route('/dashboard')
@login_required
def dashboard():
    return render_template('private/dashboard.html',
                           member={'id': session['_user_id'], 'username': session['_username']}, title="Dashboard")


@ca.route('/members', methods=['GET', 'POST'])
@login_required
def list_members():
    listing = request.args.get('list')
    members = {}

    # Filter Members according to url parameter
    if listing == 'pending':
        members = {'Pending': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'active':
        members = {'Active': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'inactive':
        members = {'Inactive': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'admin':
        members = {'Admin': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'ca_admin':
        members = {'CA Admin': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'basic':
        members = {'Basic': Member.query.filter(Member.is_verified == 0)}
    elif listing == 'role':
        all_members = Member.query.filter(Member.is_verified == 1)
        admins = [d for d in all_members if d.role == 'admin']
        ca_admins = [d for d in all_members if d.role == 'ca_admin']
        basics = [d for d in all_members if d.role == 'basic']
        members = {'Admins': admins, 'CA Admins': ca_admins, 'Basic': basics}
    elif listing == 'status':
        all_members = Member.query.filter(Member.is_verified == 1)
        active = [d for d in all_members if d.is_active]
        inactive = [d for d in all_members if not d.is_active]
        members = {'Active': active, 'Inactive': inactive}
    else:
        members = {'Current': Member.query.filter(Member.is_verified == 1, Member.is_active == 1)}

    return render_template('private/members.html', member={'id': session['_user_id'], 'username': session['_username']},
                           members=members, title='Members')


@ca.route('/members/<int:member_id>', methods=['GET', 'POST'])
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
