from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

from app.models import Team


class ActivityForm(FlaskForm):
    title = StringField('Activity Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    activityDate = StringField('Activity Date', validators=[DataRequired()])
    teams = SelectMultipleField('Team', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self):
        super(ActivityForm, self).__init__()
        self.teams.choices = [(t.id, t.name) for t in Team.query.all()]
