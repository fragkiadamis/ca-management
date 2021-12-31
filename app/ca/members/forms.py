from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


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


class BooleanForm(FlaskForm):
    status = BooleanField()
    submit = SubmitField()
