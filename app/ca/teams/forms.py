from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TeamForm(FlaskForm):
    name = StringField('Team Name', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    description = StringField('Description', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    email = StringField('Email', render_kw={'class': 'form-control', 'placeholder': ''})
    telephone = StringField('Telephone', render_kw={'class': 'form-control', 'placeholder': ''})
    submit = SubmitField('Submit')
