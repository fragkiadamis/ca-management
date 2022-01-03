from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired

from app.models import Activity


class ActivityForm(FlaskForm):
    title = StringField('Activity Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    activityDate = StringField('Activity Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_title(self, field):
        if Activity.query.filter_by(title=field.data).first():
            raise ValidationError('Activity title is already in use')
