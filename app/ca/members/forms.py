from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo

from app.models import Department, Roles


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


class EditMemberForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    ca_reg_number = StringField('CA Registration Number', validators=[DataRequired()])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')
    telephone = StringField('Telephone', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    confirm_changes = PasswordField('Password', validators=[DataRequired()])
    department = SelectField('Department', validators=[DataRequired()])
    roles = SelectMultipleField('Roles', coerce=int)
    submit = SubmitField('Update')

    def __init__(self):
        super(EditMemberForm, self).__init__()
        self.department.choices = [(d.id, d.name) for d in Department.query.all()]
        self.roles.choices = [(r.id, r.name) for r in Roles.query.all()]
