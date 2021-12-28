from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Member


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    telephone = StringField('Telephone', validators=[DataRequired()])
    semester = IntegerField('Semester', validators=[DataRequired()])
    uni_reg_number = StringField('University Registration Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    # department = SelectField('Department', validators=[DataRequired()])
    # team = SelectField('Team', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Member.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Member.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

    def validate_telephone(self, field):
        if Member.query.filter_by(telephone=field.data).first():
            raise ValidationError('Telephone is already in use.')

    def validate_uni_reg_number(self, field):
        if Member.query.filter_by(uni_reg_number=field.data).first():
            raise ValidationError('University Registration Number is already in use.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
