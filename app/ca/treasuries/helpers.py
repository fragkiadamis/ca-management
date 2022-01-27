from sqlalchemy import text
from sqlalchemy.orm import contains_eager

from app import db
from app.models import Transaction


def filter_treasuries(filter_args, treasuries):
    entities = []

    if filter_args is None:
        entities = [['Total Amount', 0, []]]
        for treasury in treasuries:
            entities[0][1] += treasury.amount
            entities[0][2] = Transaction.query.all()

        return entities

    filter_args = filter_args.split('_')
    treasury_filter = filter_args[0]
    entity_id = None
    if len(filter_args) > 1:
        entity_id = filter_args[1]

    if not entity_id:
        if treasury_filter == 'treasury':
            for treasury in treasuries:
                entities.append([treasury.name, treasury.amount, treasury.transactions])
        elif treasury_filter == 'type':
            transactions = {}
            all_transactions = Transaction.query.all()
            for transaction in all_transactions:
                if transaction.type not in transactions:
                    transactions[transaction.type] = [transaction]
                else:
                    transactions[transaction.type].append(transaction)
            for key in transactions:
                type_total_amount = 0
                for transaction in transactions[key]:
                    type_total_amount += transaction.amount
                entities.append([key, type_total_amount, transactions[key]])
    elif entity_id and entity_id.isnumeric():
        entity_id = int(entity_id)
        if treasury_filter == 'treasury':
            treasury = [t for t in treasuries if t.id == entity_id][0]
            entities.append([treasury.name, treasury.amount, treasury.transactions])

    return entities
