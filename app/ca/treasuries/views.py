from datetime import datetime

from flask import render_template, session, flash, redirect, url_for, request
from flask_login import login_required

from .forms import TransactionForm, TransferForm
from .. import ca
from ... import db
from ...decorators import permissions_required, is_not_commission
from ...filters import get_related_entities
from ...models import Transaction, Treasury, Member


@ca.route('/treasuries')
@login_required
def list_treasuries():
    filter_by = request.args.get('filter_by')
    member = Member.query.get_or_404(int(session['_user_id']))
    treasuries, *entities = get_related_entities(filter_by, member, ('Admin', 'Treasurer'), 'treasuries')
    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/treasuries/treasuries.html', user=sess_user, entities=treasuries, treasuries=entities[0], title="Treasuries")


@ca.route('/transaction/add', methods=['GET', 'POST'])
@login_required
@permissions_required(['Admin', 'Treasurer'])
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        amount = float(form.amount.data)
        treasury = Treasury.query.get_or_404(form.treasury.data)

        if form.ca_fee.data:
            if amount < 0:
                flash('The amount can not be less than 0')
                return redirect(url_for('ca.add_transaction'))

            # Create Transaction
            ca_commission = amount * .10
            transaction = Transaction(amount=amount - ca_commission, description=form.description.data, member_id=form.member.data, added_by_id=session['_user_id'], create_date=datetime.now())
            transaction.type = f'{treasury.team.name} Fee'
            treasury.amount += transaction.amount
            treasury.transactions.append(transaction)
            db.session.add(treasury)

            # Create Associated Transaction
            member = Member.query.get_or_404(transaction.member_id)
            transaction.assoc_transaction = Transaction(amount=ca_commission, description=f'Commission: {transaction.description} - {member.first_name} {member.last_name} ({member.ca_reg_number})', type='CA Commission', added_by_id=session['_user_id'], create_date=datetime.now())
            common_treasury = Treasury.query.filter(Treasury.team_id == None).first()
            common_treasury.amount += transaction.assoc_transaction.amount
            common_treasury.transactions.append(transaction.assoc_transaction)
            db.session.add(common_treasury)
        else:
            transaction = Transaction(amount=amount, description=form.description.data, added_by_id=session['_user_id'], create_date=datetime.now())
            treasury.amount += transaction.amount
            treasury.transactions.append(transaction)
            db.session.add(treasury)

        db.session.commit()

        flash('You have successfully added a new transaction.')
        return redirect(url_for('ca.list_treasuries'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/treasuries/treasury_form.html', user=sess_user, action='add', form=form, title="Add Transaction")


@ca.route('/transactions/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
@is_not_commission
@permissions_required(['Admin', 'Treasurer'])
def edit_transaction(transaction_id):
    form = TransactionForm()
    transaction = Transaction.query.get_or_404(transaction_id)

    if form.validate_on_submit():
        amount = float(form.amount.data)
        treasury = Treasury.query.get_or_404(form.treasury.data)
        current_treasury = transaction.treasury

        # If it's a registration or subscription (Common Treasury of Cultural Association gets a commission)
        if form.ca_fee.data:
            if amount < 0:
                flash('The amount can not be less than 0')
                return redirect(url_for('ca.edit_transaction'))

            ca_commission = amount * .10
            # If amount is going to different treasury
            if treasury is not current_treasury:
                # Remove from current treasury and add to new treasury
                current_treasury.amount -= transaction.amount
                current_treasury.transactions.remove(transaction)
                treasury.amount += amount - ca_commission
                treasury.transactions.append(transaction)
            else:
                # Else update treasury
                treasury.amount -= transaction.amount
                treasury.amount += amount - ca_commission

            # Update the transaction
            transaction.amount = amount - ca_commission
            transaction.type = f'{treasury.team.name} Fee'
            transaction.description = form.description.data
            transaction.member_id = form.member.data

            # And finally if there is not an associated transaction then create it; else update it
            member = Member.query.get_or_404(transaction.member_id)
            if transaction.assoc_transaction:
                transaction.assoc_transaction.description = f'Commission: {transaction.description} - {member.first_name} {member.last_name} ({member.ca_reg_number})'
                transaction.assoc_transaction.update_date = datetime.now()
                transaction.assoc_transaction.updated_by_id = session['_user_id']
            else:
                transaction.assoc_transaction = Transaction(description=f'Commission: {transaction.description} - {member.first_name} {member.last_name} ({member.ca_reg_number})', type='CA Commission', added_by_id=session['_user_id'], create_date=datetime.now())

            # Update common treasury
            common_treasury = Treasury.query.filter(Treasury.team_id == None).first()
            common_treasury.amount -= transaction.assoc_transaction.amount
            common_treasury.amount += ca_commission
            common_treasury.transactions.append(transaction.assoc_transaction)
            # Update associated transaction amount
            transaction.assoc_transaction.amount = ca_commission
        else:
            # Delete any associated transaction
            if transaction.assoc_transaction:
                transaction.assoc_transaction.treasury.amount -= transaction.assoc_transaction.amount
                db.session.delete(transaction.assoc_transaction)
            # If the amount is going to a new treasury
            if transaction.treasury is not treasury:
                # Remove from current treasury and add to new treasury
                current_treasury.amount -= transaction.amount
                current_treasury.transactions.remove(transaction)
                treasury.amount += amount
                treasury.transactions.append(transaction)
            else:
                # Else Update treasury
                treasury.amount -= transaction.amount
                treasury.amount += amount

            # Update transaction attributes
            transaction.amount = amount
            transaction.type = 'Other'
            transaction.description = form.description.data

        # Update transactions attributes
        transaction.update_date = datetime.now()
        transaction.updated_by_id = session['_user_id']
        db.session.commit()

        flash('You have successfully edited the transaction.')
        return redirect(url_for('ca.list_treasuries'))

    sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
    return render_template('private/treasuries/treasury_form.html', user=sess_user, transaction=transaction, action='edit', form=form, title="Edit Transaction")


@ca.route('/transactions/delete/<int:transaction_id>')
@login_required
@is_not_commission
@permissions_required(['Admin', 'Treasurer'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    treasury = transaction.treasury
    treasury.amount -= transaction.amount
    treasury.transactions.remove(transaction)
    if transaction.assoc_transaction:
        common_treasury = Treasury.query.filter(Treasury.team_id == None).first()
        common_treasury.amount -= transaction.assoc_transaction.amount
        common_treasury.transactions.remove(transaction.assoc_transaction)

    db.session.delete(transaction)
    db.session.commit()

    flash('You have successfully deleted the transaction.')
    return redirect(url_for('ca.list_treasuries'))


# @ca.route('/transactions/transfer', methods=['GET', 'POST'])
# @login_required
# def transfer_money():
#     form = TransferForm()
#     if form.validate_on_submit():
#         amount = float(form.amount.data)
#         from_treasury = Treasury.query.get_or_404(form.from_treasury.data)
#         to_treasury = Treasury.query.get_or_404(form.to_treasury.data)
#
#         if amount < 0:
#             flash('The amount can not be less than 0')
#             return redirect(url_for('ca.transfer_money'))
#         if amount > from_treasury.amount:
#             flash('There are not sufficient funds')
#             return redirect(url_for('ca.transfer_money'))
#
#         from_treasury.amount -= amount
#         from_treasury.transactions.append(Transaction(amount=-amount, description=f'Transfer to {to_treasury.name}', type='Transfer', added_by_id=session['_user_id'], create_date=datetime.now()))
#         to_treasury.amount += amount
#         to_treasury.transactions.append(Transaction(amount=amount, description=f'Transfer from {from_treasury.name}', type='Transfer', added_by_id=session['_user_id'], create_date=datetime.now()))
#
#         db.session.commit()
#
#         flash('You have successfully transferred money.')
#         return redirect(url_for('ca.list_treasuries'))
#
#     sess_user = {'id': session['_user_id'], 'username': session['_username'], 'roles': session['_user_roles']}
#     return render_template('private/treasuries/treasury_form.html', user=sess_user, action='transfer', form=form, title="Transfer Money")
