from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired

from app.models import Announcement


class AnnouncementForm(FlaskForm):
    title = StringField('Announcement Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    createDate = StringField('Create Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_title(self, field):
        if Announcement.query.filter_by(title=field.data).first():
            raise ValidationError('Announcement title is already in use')
