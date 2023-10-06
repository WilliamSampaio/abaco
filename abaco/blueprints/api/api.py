import json
from io import BytesIO

from babel.numbers import format_percent
from flask import Blueprint, request
from flask_babel import format_currency
from flask_babel import gettext as _

from abaco.database import db_filename, validate_schema
from abaco.localization import get_locale
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
    with open(db_filename, 'w') as database_file:
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
    if user_config.save() is None:
        return {'message': _('Failed to update data')}, 400
    return {'message': _('Abaco database updated successfully')}, 200


@api.route('/fixed-discounts', methods=['GET'])
def getall_fixed_discounts():
    results = []
    for discount in FixedDiscount().available():
        if discount['calculated_in'] == 'value':
            discount['value'] = format_currency(
                discount['value'], UserConfig().find(1).currency
            )
        else:
            discount['value'] = format_percent(
                discount['value'] / 100,
                locale=get_locale(),
                decimal_quantization=False,
            )
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
    transactions = Transaction().between(
        data['initial_date'], data['final_date']
    )
    fixed_discounts = FixedDiscount().all()
    earnings = 0
    expenses = 0
    for transaction in transactions:
        if transaction['expense']:
            expenses += transaction['value']
            continue
        if len(transaction['fixed_discounts_ids']) > 0:
            discounts = 0
            for discount in fixed_discounts:
                if discount['id'] in transaction['fixed_discounts_ids']:
                    discounts += discount['value']
            earnings += transaction['value'] - discounts
            continue
        earnings += transaction['value']
    balance = earnings - expenses
    results = {
        'transactions': transactions,
        'totals': {
            'earnings': format_currency(
                earnings, UserConfig().find(1).currency
            ),
            'expenses': format_currency(
                expenses, UserConfig().find(1).currency
            ),
            'balance': format_currency(balance, UserConfig().find(1).currency),
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
