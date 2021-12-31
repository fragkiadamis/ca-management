from flask import render_template, session, flash, request, redirect, url_for
from flask_login import login_required

from .. import ca
from .forms import ProfileForm, BooleanForm
from app.ca.members.model import Member


@ca.route('/members', methods=['GET', 'POST'])
@login_required
def list_members():
    display = request.args.get('display')
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'role': session['_user_role']}

    # Filter Members according to url parameter
    members = Member.filter_members(display)

    return render_template('private/members.html', boolean_form=BooleanForm(), user=sess_user, members=members, title='Members', display=display)


@ca.route('/members/<int:member_id>', methods=['GET', 'POST'])
@login_required
def profile(member_id):
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'role': session['_user_role']}

    form = ProfileForm()
    member = Member.query.get_or_404(member_id)

    if form.validate_on_submit():
        if not member.verify_password(form.confirm_changes.data):
            flash('Invalid Password')
            return render_template('private/profile.html', form=form, user=sess_user, title='Profile')

        # Update member properties
        member.update_data(form)
        flash('You have successfully updated your profile.')

    return render_template('private/profile.html', form=form, member=member, user=sess_user, title='Profile')


@ca.route('/status/<int:member_id>', methods=['GET', 'POST'])
@login_required
def toggle_status(member_id):
    form = BooleanForm()
    if form.validate_on_submit():
        display = request.args.get('display')
        member = Member.query.get_or_404(member_id)
        member.toggle_status(form)

    return redirect(url_for('ca.list_members', display=display))


@ca.route('/verify/<int:member_id>', methods=['POST'])
@login_required
def verify(member_id):
    form = BooleanForm()
    if form.validate_on_submit():
        member = Member.query.get_or_404(member_id)
        if form.status.data:
            member.verify()
        else:
            member.delete()

    return redirect(url_for('ca.list_members', display='pending'))