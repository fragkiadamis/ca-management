from flask import render_template, session, flash, redirect, url_for
from flask_login import login_required

from .forms import TransactionForm
from .. import ca
from ... import db
from ...decorators import permissions_required
from ...models import Team, Transaction


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
        transaction = Transaction(amount=form.amount.data, description=form.description.data, type=form.type.data, member=form.member.data, team=form.team.data, added_by=session['_user_id'])
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
        transaction.amount = form.amount.data
        transaction.description = form.description.data
        transaction.type = form.type.data
        transaction.member = form.member.data
        transaction.team = form.team.data
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
