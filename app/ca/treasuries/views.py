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
    transactions = Transaction.query.all()
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/treasuries/treasuries.html', user=sess_user, transactions=transactions, title="Treasuries")


@ca.route('/transaction/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        amount = float(form.amount.data)
        if (form.type.data == 'registration') or (form.type.data == 'subscription'):
            ca_commission = amount * .10
            transaction = Transaction(amount=amount - ca_commission, description=form.description.data, type=form.type.data, member=form.member.data, team_id=form.team.data, added_by_id=session['_user_id'], create_date=datetime.now())
            transaction.commission = Commission(amount=ca_commission, description=f'10% from {form.type.data}')
            db.session.add(transaction)
            db.session.commit()
        else:
            transaction = Transaction(amount=amount, description=form.description.data, type=form.type.data, team=form.team.data, added_by=session['_user_id'])
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
        if (form.type.data == 'registration') or (form.type.data == 'subscription'):
            ca_commission = amount * .10
            transaction.amount = amount - ca_commission
            transaction.commission = Commission(amount=ca_commission, description=f'10% from {form.type.data}')
        else:
            transaction.commission = None

        transaction.description = form.description.data
        transaction.update_date = datetime.now()
        transaction.updated_by = session['_user_id']
        transaction.team_id = form.team.data
        transaction.type = form.type.data
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
