from datetime import datetime

from flask import render_template, session, flash, redirect, url_for
from flask_login import login_required

from .forms import TransactionForm
from .. import ca
from ... import db
from ...decorators import permissions_required
from ...models import Team, Transaction, Commission, Member


@ca.route('/treasuries')
@login_required
def list_treasuries():
    # transactions = {'All': Transaction.query.all()}
    all_transactions = Transaction.query.all()
    treasuries = {'Cultural Association': 0}
    for transaction in all_transactions:
        if transaction.team:
            if transaction.team.name not in treasuries:
                treasuries[transaction.team.name] = 0
            treasuries[transaction.team.name] += transaction.amount
            if transaction.commission:
                treasuries['Cultural Association'] += transaction.commission.amount
        else:
            treasuries['Cultural Association'] += transaction.amount

    transactions = {'All': all_transactions}
    teams = Team.query.all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/treasuries/treasuries.html', user=sess_user, transactions=transactions, treasuries=treasuries, teams=teams, title="Treasuries")


@ca.route('/transaction/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        amount = float(form.amount.data)
        if form.type.data:
            ca_commission = amount * .10
            transaction = Transaction(amount=amount - ca_commission, description=form.description.data, type='CA Fee', member_id=form.member.data, added_by_id=session['_user_id'], create_date=datetime.now())
            print(form.team.data, type(form.team.data))
            transaction.commission = Commission(amount=ca_commission, description='10% commission')
        else:
            transaction = Transaction(amount=amount, description=form.description.data, added_by_id=session['_user_id'], create_date=datetime.now())

        transaction.team_id = form.team.data if int(form.team.data) else None
        db.session.add(transaction)
        db.session.commit()

        flash('You have successfully added a new transaction.')
        return redirect(url_for('ca.list_treasuries'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/treasuries/treasury_form.html', user=sess_user, action='add', form=form, title="Add Transaction")


@ca.route('/transactions/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    form = TransactionForm()
    transaction = Transaction.query.get_or_404(transaction_id)
    if form.validate_on_submit():
        amount = float(form.amount.data)
        if form.type.data:
            ca_commission = amount * .10
            transaction.amount = amount - ca_commission
            transaction.type = 'CA Fee'
            transaction.commission = Commission(amount=ca_commission, description='10% commission')
            transaction.member_id = form.member.data
        else:
            transaction.amount = amount
            transaction.commission = None
            transaction.type = 'Other'

        transaction.team_id = form.team.data if int(form.team.data) else None
        transaction.description = form.description.data
        transaction.update_date = datetime.now()
        transaction.updated_by_id = session['_user_id']
        db.session.commit()

        flash('You have successfully edited the transaction.')
        return redirect(url_for('ca.list_treasuries'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/treasuries/treasury_form.html', user=sess_user, transaction=transaction, action='edit', form=form, title="Edit Transaction")


@ca.route('/transactions/delete/<int:transaction_id>')
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()

    flash('You have successfully deleted the transaction.')
    return redirect(url_for('ca.list_treasuries'))
