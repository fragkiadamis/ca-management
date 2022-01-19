from datetime import datetime, date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, DateField, TimeField
from wtforms.validators import DataRequired, Optional

from app.models import Team


class ActivityForm(FlaskForm):
    title = StringField('Activity Name', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    description = StringField('Description', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    start_date = DateField('Start Date', render_kw={'class': 'form-control', 'placeholder': ''}, default=date.today, validators=[DataRequired("Please enter the start date.")])
    end_date = DateField('Start Date', render_kw={'class': 'form-control', 'placeholder': ''}, default=date.today, validators=[DataRequired("Please enter the end date.")])
    start_time = TimeField('Start Time', render_kw={'class': 'form-control', 'placeholder': ''}, format='%H:%M:%S', default=datetime.now(), validators=[DataRequired("Please enter the start time.")])
    end_time = TimeField('End Time', render_kw={'class': 'form-control', 'placeholder': ''}, format='%H:%M:%S', default=datetime.now(), validators=[DataRequired("Please enter the end time.")])
    teams = SelectMultipleField('Team', render_kw={'class': 'form-control', 'placeholder': ''}, coerce=int)
    submit = SubmitField('Submit')

    def __init__(self):
        super(ActivityForm, self).__init__()
        self.teams.choices = [(t.id, t.name) for t in Team.query.all()]
        self.teams.size = len(self.teams.choices) if self.teams else 3
