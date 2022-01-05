from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired


class ActivityForm(FlaskForm):
    title = StringField('Activity Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    activityDate = StringField('Activity Date', validators=[DataRequired()])
    submit = SubmitField('Submit')
