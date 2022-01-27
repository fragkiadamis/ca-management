from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired

from app.models import Team, Member, Treasury


class TransactionForm(FlaskForm):
    amount = StringField('Amount', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    description = StringField('Description', render_kw={'class': 'form-control', 'placeholder': ''})
    ca_fee = BooleanField('Registration / Subscription')
    treasury = SelectField('Team Treasury', render_kw={'class': 'form-control', 'placeholder': ''}, coerce=int)
    member = SelectField('Member', render_kw={'class': 'form-control', 'placeholder': ''}, coerce=int)
    submit = SubmitField('Submit')

    def __init__(self):
        super(TransactionForm, self).__init__()
        active_members = Member.query.filter(Member.is_active).all()
        all_treasuries = Treasury.query.all()
        self.member.choices = [(m.id, f'{m.first_name} {m.last_name}, ({m.ca_reg_number})') for m in active_members]
        self.treasury.choices = [(t.id, f'{t.name} ({t.amount} euros)') for t in all_treasuries]


class TransferForm(FlaskForm):
    amount = StringField('Amount', render_kw={'class': 'form-control', 'placeholder': ''}, validators=[DataRequired()])
    from_treasury = SelectField('From', render_kw={'class': 'form-control', 'placeholder': ''})
    to_treasury = SelectField('To', render_kw={'class': 'form-control', 'placeholder': ''})
    submit = SubmitField('Submit')

    def __init__(self):
        super(TransferForm, self).__init__()
        all_treasuries = Treasury.query.all()
        self.from_treasury.choices = [(t.id, f'{t.name} ({t.amount} euros)') for t in all_treasuries]
        self.to_treasury.choices = [(t.id, f'{t.name} ({t.amount} euros)') for t in all_treasuries]
