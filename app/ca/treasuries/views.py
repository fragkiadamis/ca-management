from datetime import datetime

from flask import render_template, session, flash, redirect, url_for, request
from flask_login import login_required

from .forms import TransactionForm, TransferForm
from .helpers import filter_treasuries
from .. import ca
from ... import db
from ...decorators import permissions_required, is_not_transfer
from ...models import Team, Transaction


@ca.route('/treasuries')
@login_required
def list_treasuries():
    filter_by = request.args.get('filter_by')
    teams = Team.query.all()
    treasuries, transactions = filter_treasuries(filter_by, teams)

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
            transaction = Transaction(amount=amount - ca_commission, description=form.description.data, type='CA Fee', member_id=form.member.data, added_by_id=session['_user_id'], team_id=form.team.data, create_date=datetime.now())
            transaction.assoc_transaction = Transaction(amount=ca_commission, description=f'{form.description.data} (commission)', team_id=1, type='CA Commission')
        else:
            transaction = Transaction(amount=amount, description=form.description.data, team_id=form.team.data, added_by_id=session['_user_id'], create_date=datetime.now())

        db.session.add(transaction)
        db.session.commit()

        flash('You have successfully added a new transaction.')
        return redirect(url_for('ca.list_treasuries'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/treasuries/treasury_form.html', user=sess_user, action='add', form=form, title="Add Transaction")


@ca.route('/transactions/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
@is_not_transfer
def edit_transaction(transaction_id):
    form = TransactionForm()
    transaction = Transaction.query.get_or_404(transaction_id)
    if form.validate_on_submit():
        amount = float(form.amount.data)
        if form.type.data:
            ca_commission = amount * .10
            transaction.amount = amount - ca_commission
            transaction.type = 'CA Fee'
            transaction.assoc_transaction = Transaction(amount=ca_commission, team_id=1, description=f'{form.description.data} (commission)', type='CA Commission')
            transaction.member_id = form.member.data
        else:
            transaction.amount = amount
            transaction.assoc_transaction = None
            transaction.type = 'Other'

        transaction.team_id = form.team.data
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
@is_not_transfer
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()

    flash('You have successfully deleted the transaction.')
    return redirect(url_for('ca.list_treasuries'))


@ca.route('/transactions/transfer', methods=['GET', 'POST'])
@login_required
def transfer_money():
    form = TransferForm()
    if form.validate_on_submit():
        amount = float(form.amount.data)
        from_team = Team.query.get_or_404(form.from_team.data)
        to_team = Team.query.get_or_404(form.to_team.data)

        if amount > from_team.treasury:
            flash('There are not sufficient funds')
            return redirect(url_for('ca.transfer_money'))

        transfer = Transaction(amount=-amount, description=f'Transfer to {to_team.name}', type='Transfer', added_by_id=session['_user_id'], team_id=form.from_team.data, create_date=datetime.now())
        transfer.assoc_transaction = Transaction(amount=amount, description=f'Transfer from {from_team.name}', team_id=form.to_team.data, type='Transfer')
        db.session.add(transfer)
        db.session.commit()

        flash('You have successfully transferred money.')
        return redirect(url_for('ca.list_treasuries'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/treasuries/treasury_form.html', user=sess_user, action='transfer', form=form, title="Transfer Money")
