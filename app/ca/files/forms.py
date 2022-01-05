from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, FileField
from wtforms.validators import DataRequired

from app.models import Team


class FileForm(FlaskForm):
    file_field = FileField('ASD', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    teams = SelectMultipleField('Team', render_kw={'class': 'form-control', 'placeholder': ''}, coerce=int)
    submit = SubmitField('Submit')

    def __init__(self):
        super(FileForm, self).__init__()
        self.teams.choices = [(t.id, t.name) for t in Team.query.all()]
        self.teams.size = len(self.teams.choices) if self.teams else 3
