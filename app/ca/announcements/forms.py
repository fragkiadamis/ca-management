from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired

from app.models import Team


class AnnouncementForm(FlaskForm):
    title = StringField('Title', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    body = TextAreaField('Announcement', render_kw={'class': 'form-control', 'placeholder': '', 'rows': 15}, validators=[DataRequired()])
    teams = SelectMultipleField('Team', render_kw={'class': 'form-control', 'placeholder': ''}, coerce=int)
    submit = SubmitField('Submit')

    def __init__(self):
        super(AnnouncementForm, self).__init__()
        self.teams.choices = [(t.id, t.name) for t in Team.query.all()]
        self.teams.size = len(self.teams.choices) if self.teams else 3
