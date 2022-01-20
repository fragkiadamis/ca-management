from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired

from app.models import Team, Member


class TransactionForm(FlaskForm):
    amount = StringField('Amount', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    description = StringField('Description', render_kw={'class': 'form-control', 'placeholder': ''})
    type = RadioField('Team', choices=[('other', 'Other'), ('registration', 'Registration'), ('subscription', 'Subscription')], validators=[DataRequired()])
    team = SelectField('Team', render_kw={'class': 'form-control', 'placeholder': ''})
    member = SelectField('Member', render_kw={'class': 'form-control', 'placeholder': ''})
    submit = SubmitField('Submit')

    def __init__(self):
        super(TransactionForm, self).__init__()
        self.member.choices = [(m.id, f'{m.first_name} {m.last_name}, ({m.ca_reg_number})') for m in Member.query.all()]
        self.team.choices = [('', 'Cultural Association')]
        teams = Team.query.all()
        for team in teams:
            self.team.choices.append((team.id, team.name))
