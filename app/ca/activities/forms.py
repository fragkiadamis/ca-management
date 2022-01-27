from datetime import datetime, date, time
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, DateTimeLocalField, TextAreaField
from wtforms.validators import DataRequired, Optional, ValidationError

from app.models import Team


class ActivityForm(FlaskForm):
    title = StringField('Activity Name', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    body = TextAreaField('Body', render_kw={'class': 'form-control', 'placeholder': '', 'style': "height: 200px"}, validators=[DataRequired()])
    start_date = DateTimeLocalField('Start Date', render_kw={'class': 'form-control', 'placeholder': ''}, default=datetime.now(), format='%Y-%m-%dT%H:%M', validators=[DataRequired("Please enter the start date.")])
    end_date = DateTimeLocalField('End Date', render_kw={'class': 'form-control', 'placeholder': ''}, default=datetime.now(), format='%Y-%m-%dT%H:%M', validators=[DataRequired("Please enter the end date.")])
    teams = SelectMultipleField('Team', render_kw={'class': 'form-control', 'placeholder': ''}, coerce=int)
    submit = SubmitField('Submit')

    def __init__(self):
        super(ActivityForm, self).__init__()
        self.teams.choices = [(t.id, t.name) for t in Team.query.all()]
        self.teams.size = len(self.teams.choices) if self.teams else 3

    def validate_end_date(self, field):
        if field.data < self.start_date.data:
            raise ValidationError("End date must not be earlier than start date.")
