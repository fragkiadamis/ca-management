from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

from app.models import Team


class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    teams = SelectMultipleField('Team', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self):
        super(AnnouncementForm, self).__init__()
        self.teams.choices = [(t.id, t.name) for t in Team.query.all()]
