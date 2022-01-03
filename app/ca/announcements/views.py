from flask import render_template, session, flash, redirect, url_for
from flask_login import login_required

from .forms import AnnouncementForm
from .. import ca
from ... import db
from ...decorators import permissions_required
from ...models import Announcement


@ca.route('/dashboard/announcements', methods=['GET', 'POST'])
@login_required
def list_announcements():
    announcements = Announcement.query.all()

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/dashboard.html',
                           user=sess_user,
                           announcements=announcements,
                           title="Dashboard")


@ca.route('/dashboard/announcements/<int:announcement_id>', methods=['GET', 'POST'])
@login_required
def get_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/dashboard.html',
                           user=sess_user,
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
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/announcement-actions.html',
                           action="Add", add_announcement=add_announcement, form=form,
                           user=sess_user,
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

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/announcement-actions.html', action="Edit",
                           add_announcement=add_announcement, form=form, announcement=announcement,
                           user=sess_user,
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
