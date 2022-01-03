from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from app.models import School


class UniEntityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Add School')


class EditDepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    schools = SelectField('School', validators=[DataRequired()])
    submit = SubmitField('Add Department')

    def __init__(self):
        super(EditDepartmentForm, self).__init__()
        self.schools.choices = [(s.id, s.name) for s in School.query.all()]
