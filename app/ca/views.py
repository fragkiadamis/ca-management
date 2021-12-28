from flask import render_template
from flask_login import login_required

from . import admin


@admin.route('/dashboard')
@login_required
def dashboard():
    return render_template('private/dashboard.html', title="Dashboard")
