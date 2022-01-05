from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

from app.models import Team


class FileForm(FlaskForm):
    name = StringField('File Name', validators=[DataRequired()])
    path = StringField('Path', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    teams = SelectMultipleField('Team', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self):
        super(FileForm, self).__init__()
        self.teams.choices = [(t.id, t.name) for t in Team.query.all()]
