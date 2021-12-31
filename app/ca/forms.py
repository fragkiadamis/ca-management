from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField, SelectField, \
    SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Member, Team, Activity, Announcement


class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    telephone = StringField('Telephone', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    confirm_changes = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update')


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


class ActivityForm(FlaskForm):
    title = StringField('Activity Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    createDate = StringField('Create Date', validators=[DataRequired()])
    activityDate = StringField('Activity Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_title(self, field):
        if Activity.query.filter_by(title=field.data).first():
            raise ValidationError('Activity title is already in use')


class AnnouncementForm(FlaskForm):
    title = StringField('Announcement Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    createDate = StringField('Create Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_title(self, field):
        if Announcement.query.filter_by(title=field.data).first():
            raise ValidationError('Announcement title is already in use')

