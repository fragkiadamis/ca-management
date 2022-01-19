from flask import render_template, session, flash, redirect, url_for
from flask_login import login_required

from .forms import AnnouncementForm
from .. import ca
from ... import db
from ...decorators import permissions_required
from ...models import Announcement, Team


@ca.route('/announcements')
@login_required
def list_announcements():
    announcements = Announcement.query.all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/announcements/announcements.html', user=sess_user, announcements=announcements, title="Announcements")


@ca.route('/announcements/add', methods=['GET', 'POST'])
@login_required
def add_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, body=form.body.data, added_by=session['_user_id'])
        for team_id in form.teams.data:
            announcement.teams.append(Team.query.get_or_404(team_id))
        db.session.add(announcement)
        db.session.commit()

        flash('You have successfully added a new announcement.')
        return redirect(url_for('ca.list_announcements'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/announcements/announcement_form.html', user=sess_user, action='add', form=form, title="Add Announcement")


@ca.route('/announcements/edit/<int:announcement_id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(announcement_id):
    form = AnnouncementForm()
    announcement = Announcement.query.get_or_404(announcement_id)
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.body = form.body.data
        announcement.teams = []
        for team_id in form.teams.data:
            announcement.teams.append(Team.query.get_or_404(team_id))
        db.session.commit()

        flash('You have successfully edited the announcement.')
        return redirect(url_for('ca.list_announcements'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/announcements/announcement_form.html', user=sess_user, announcement=announcement, action='edit', form=form, title="Edit Announcement")


@ca.route('/announcements/delete/<int:announcement_id>')
@login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    db.session.delete(announcement)
    db.session.commit()

    flash('You have successfully deleted the announcement.')
    return redirect(url_for('ca.list_announcements'))
