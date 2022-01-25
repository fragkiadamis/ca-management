from app.models import Transaction


def filter_treasuries(filter_args, teams):
    treasuries = {}
    transactions = {}

    if filter_args is None:
        treasuries = {'Total': 0}
        for team in teams:
            treasuries['Total'] += team.treasury
            treasuries[team.name] = team.treasury
        transactions = {'All': Transaction.query.all()}

        return treasuries, transactions

    filter_args = filter_args.split('_')
    treasury_filter = filter_args[0]
    entity_id = None
    if len(filter_args) > 1:
        entity_id = filter_args[1]

    if not entity_id:
        if treasury_filter == 'team':
            all_transactions = Transaction.query.all()
            for team in teams:
                treasuries[team.name] = team.treasury
            for transaction in all_transactions:
                if transaction.team.name not in transactions:
                    transactions[transaction.team.name] = [transaction]
                else:
                    transactions[transaction.team.name].append(transaction)
        elif treasury_filter == 'type':
            all_transactions = Transaction.query.all()
            for team in teams:
                treasuries[team.name] = team.treasury
            for transaction in all_transactions:
                if transaction.type not in transactions:
                    transactions[transaction.type] = [transaction]
                else:
                    transactions[transaction.type].append(transaction)
    elif entity_id and entity_id.isnumeric():
        entity_id = int(entity_id)
        if treasury_filter == 'team':
            team = [t for t in teams if t.id == entity_id][0]
            treasuries[team.name] = team.treasury
            transactions[team.name] = Transaction.query.filter(Transaction.team == team).all()

    return treasuries, transactions
