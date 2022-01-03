from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired

from app.models import Team


class TeamForm(FlaskForm):
    name = StringField('Team Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    telephone = StringField('Telephone', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if Team.query.filter_by(name=field.data).first():
            raise ValidationError('Name is already in use')

    def validate_email(self, field):
        if Team.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_telephone(self, field):
        if Team.query.filter_by(telephone=field.data).first():
            raise ValidationError('Telephone is already in use.')
