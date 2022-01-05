from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class FileForm(FlaskForm):
    name = StringField('File Name', validators=[DataRequired()])
    path = StringField('Path', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    submit = SubmitField('Submit')
