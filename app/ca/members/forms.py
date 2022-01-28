from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo

from app.models import Department, Role, Team


class ProfileForm(FlaskForm):
    first_name = StringField('First Name', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    last_name = StringField('Last Name', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    username = StringField('Username', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    email = StringField('Email', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password', render_kw={'class': 'form-control', 'placeholder': ''})
    telephone = StringField('Telephone', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    city = StringField('City', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    address = StringField('Address', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    confirm_changes = PasswordField('Password', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    submit = SubmitField('Update')


class EditMemberForm(FlaskForm):
    first_name = StringField('First Name', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    last_name = StringField('Last Name', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    username = StringField('Username', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    email = StringField('Email', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired(), Email()])
    ca_reg_number = StringField('CA Registration Number', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    password = PasswordField('Password', render_kw={'class': 'form-control', 'placeholder': ''})
    confirm_password = PasswordField('Confirm Password', render_kw={'class': 'form-control', 'placeholder': ''})
    telephone = StringField('Telephone', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    city = StringField('City', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    address = StringField('Address', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    confirm_changes = PasswordField('Password', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    department = SelectField('Department', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    roles = SelectMultipleField('Roles', render_kw={'class': 'form-control', 'placeholder': ''}, coerce=int)
    teams = SelectMultipleField('Team', render_kw={'class': 'form-control', 'placeholder': ''}, coerce=int)
    submit = SubmitField('Update')

    def __init__(self):
        super(EditMemberForm, self).__init__()
        self.department.choices = [(d.id, d.name) for d in Department.query.all()]
        self.roles.choices = [(r.id, r.name) for r in Role.query.all()]
        self.roles.size = len(self.roles.choices) if self.roles else 3
        self.teams.choices = [(t.id, t.name) for t in Team.query.all()]
        self.teams.size = len(self.teams.choices) if self.teams else 3
