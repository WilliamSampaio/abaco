import json
from io import BytesIO

from flask import Blueprint, request
from flask_babel import gettext as _

from abaco.database import db_path, validate_schema
from abaco.localization import format_currency, format_percent
from abaco.models import FixedDiscount, Transaction, UserConfig
from abaco.utils import validate_json

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/new-abaco', methods=['POST'])
def new_abaco():
    data = request.get_json()
    user_config = UserConfig(data['name'], data['language'], data['currency'])
    if user_config.save() is None:
        return {'message': _('Failed to save data')}, 400
    return {'message': _('Abaco created successfully')}, 201


@api.route('/import-abaco', methods=['POST'])
def import_abaco():
    if 'database' not in request.files.keys():
        return {'message': _('Database file not sent')}, 400
    database = BytesIO(request.files.get('database').stream.read())
    # print(type(database.getvalue().decode()))
    # print(database.getvalue().decode())
    database_dict = None
    if validate_json(database.getvalue().decode()):
        database_dict = json.loads(database.getvalue().decode())
    else:
        return {'message': _('Database invalid')}, 400
    if not validate_schema(database_dict):
        return {'message': _('Database invalid')}, 400
    # print(type(database_dict))
    # print(database_dict)
    with open(db_path, 'w') as database_file:
        database_file.write(json.dumps(database_dict))
    return {'message': _('Abaco database imported successfully')}, 201


@api.route('/settings', methods=['UPDATE'])
def settings():
    data = request.get_json()
    user_config = UserConfig().find(1)
    if user_config is None:
        return {'message': _('Failed to update data')}, 400
    user_config.name = data['name']
    user_config.language = data['language']
    user_config.currency = data['currency']
    user_config.dark_mode = data['dark_mode']
    if user_config.save() is None:
        return {'message': _('Failed to update data')}, 400
    return {'message': _('Abaco database updated successfully')}, 200


@api.route('/fixed-discounts', methods=['GET'])
def getall_fixed_discounts():
    results = []
    for discount in FixedDiscount().available():
        if discount['calculated_in'] == 'value':
            discount['value'] = format_currency(discount['value'])
        else:
            discount['value'] = format_percent(discount['value'])
        results.append(discount)
    return {'fixed_discounts': results}, 200


@api.route('/fixed-discount', methods=['POST'])
def post_fixed_discount():
    data = request.get_json()
    fixed_discount = FixedDiscount(
        data['description'], data['calculated_in'], data['value']
    )
    if fixed_discount.save() is None:
        return {'message': _('Failed to save data')}, 400
    return {'message': _('Fixed discount successfully registered!')}, 201


@api.route('/fixed-discount/<int:id>', methods=['DELETE'])
def delete_fixed_discount(id):
    fixed_discount = FixedDiscount().find(id)
    if fixed_discount is None:
        return {'message': _('Failed to delete data')}, 404
    fixed_discount.deleted = True
    if fixed_discount.save() is None:
        return {'message': _('Failed to delete data')}, 400
    return {'message': _('Fixed discount successfully deleted!')}, 200


@api.route('/transaction', methods=['POST'])
def post_transaction():
    data = request.get_json()
    transaction = Transaction(
        data['description'],
        data['date'],
        data['value'],
        data['expense'],
        data['fixed_discounts_ids'],
    )
    if transaction.save() is None:
        return {'message': _('Failed to save data')}, 400
    return {'message': _('Transaction successfully registered!')}, 201


@api.route('/transactions', methods=['POST'])
def getall_transaction():
    data = request.get_json()
    if 'all' in data and data['all'] is True:
        transactions = Transaction().all(order_by='date')
    else:
        transactions = Transaction().between(
            data['initial_date'], data['final_date']
        )
    fixed_discounts = FixedDiscount().all()
    earnings = 0
    expenses = 0
    new_transactions = []
    for transaction in transactions:
        if transaction['expense']:
            expenses += transaction['value']
            new_transactions.append(transaction)
            continue
        if len(transaction['fixed_discounts_ids']) > 0:
            discounts = 0
            for discount in fixed_discounts:
                if discount['id'] in transaction['fixed_discounts_ids']:
                    if discount['calculated_in'] == 'porcentage':
                        discounts += (discount['value'] / 100) * transaction[
                            'value'
                        ]
                    else:
                        discounts += discount['value']
            earnings += transaction['value'] - discounts
            transaction['net_value'] = transaction['value'] - discounts
            transaction['discounts'] = discounts
            new_transactions.append(transaction)
            continue
        earnings += transaction['value']
        new_transactions.append(transaction)
    balance = earnings - expenses
    results = {
        'user_config': UserConfig().find(1).as_dict(),
        'initial_date': transactions[0]['date'],
        'final_date': transactions[-1]['date'],
        'transactions': new_transactions,
        'totals': {
            'earnings': earnings,
            'expenses': expenses,
            'balance': balance,
        },
    }
    return {'results': results}, 200


@api.route('/transaction/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Transaction().find(id)
    if transaction is None:
        return {'message': _('Failed to get data')}, 404
    return {'transaction': transaction.as_dict()}, 200


@api.route('/transaction/<int:id>', methods=['UPDATE'])
def update_transaction(id):
    data = request.get_json()
    transaction = Transaction().find(id)
    if transaction is None:
        return {'message': _('Failed to update data')}, 400
    transaction.description = data['description']
    transaction.date = data['date']
    transaction.value = data['value']
    transaction.expense = data['expense']
    transaction.fixed_discounts_ids = data['fixed_discounts_ids']
    if transaction.save() is None:
        return {'message': _('Failed to update data')}, 400
    return {'message': _('Transaction updated successfully')}, 200


@api.route('/transaction/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transaction().find(id)
    if transaction is None:
        return {'message': _('Failed to delete data')}, 404
    if transaction.delete() is None:
        return {'message': _('Failed to delete data')}, 400
    return {'message': _('Transaction successfully deleted!')}, 200
