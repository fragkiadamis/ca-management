from flask import render_template, session, flash, redirect, url_for, request
from flask_login import login_required

from .forms import AnnouncementForm
from .. import ca
from ... import db
from ...decorators import permissions_required
from ...filters import filter_entities
from ...models import Announcement, Team


@ca.route('/announcements')
@login_required
def list_announcements():
    filter_by = request.args.get('filter_by')
    announcements = Announcement.query.all()
    teams = Team.query.all()
    entities = filter_entities(filter_by, announcements, teams)
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/announcements/announcements.html', user=sess_user, announcements=entities, teams=teams, title="Announcements")


@ca.route('/announcement/<int:announcement_id>')
@login_required
def get_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}

    return render_template('private/announcements/single_announcement.html',
                           user=sess_user,
                           announcement=announcement,
                           title="Dashboard")


@ca.route('/announcements/add', methods=['GET', 'POST'])
@login_required
@permissions_required(['Admin', 'Editor'])
def add_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, added_by_id=session['_user_id'])
        announcement.body = form.body.data.replace('<br>', '\n')
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
@permissions_required(['Admin', 'Editor'])
def edit_announcement(announcement_id):
    form = AnnouncementForm()
    announcement = Announcement.query.get_or_404(announcement_id)
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.body = form.body.data.replace('<br>', '\n')
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
@permissions_required(['Admin', 'Editor'])
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    db.session.delete(announcement)
    db.session.commit()

    flash('You have successfully deleted the announcement.')
    return redirect(url_for('ca.list_announcements'))
