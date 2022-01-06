from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

from app.models import Member, Team
from app.models import Department


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    last_name = StringField('Last Name', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    username = StringField('Username', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    email = StringField('Email', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[
        DataRequired(),
        EqualTo('confirm_password')
    ])
    confirm_password = PasswordField('Confirm Password', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    telephone = StringField('Telephone', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    uni_reg_number = StringField('University Registration Number', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    city = StringField('City', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    address = StringField('Address', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    department = SelectField('Department', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    teams = SelectMultipleField('Team', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()], coerce=int)
    submit = SubmitField('Register')

    def __init__(self):
        super(RegistrationForm, self).__init__()
        self.department.choices = [(d.id, d.name) for d in Department.query.all()]
        self.teams.choices = [(t.id, t.name) for t in Team.query.all()]
        self.teams.size = len(self.teams.choices) if self.teams else 3

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
    email = StringField('Email', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')
