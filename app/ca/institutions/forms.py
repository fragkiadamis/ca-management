from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UniEntityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    abbreviation = StringField('Abbreviation')
    submit = SubmitField('Add')
