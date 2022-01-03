from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models import File


class FileForm(FlaskForm):
    name = StringField('File Name', validators=[DataRequired()])
    path = StringField('Path', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    submit = SubmitField('Upload')

    def validate_name(self, field):
        if File.query.filter_by(name=field.data).first():
            raise ValidationError('Name is already in use')
