import json
from io import BytesIO

from babel.numbers import format_percent
from flask import Blueprint, request
from flask_babel import format_currency
from flask_babel import gettext as _

from abaco.classes import UserConfig
from abaco.database import (
    db_filename,
    get_fixed_discounts,
    get_query,
    get_user_config,
    validate_schema,
)
from abaco.localization import get_locale
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
    db_fixed_discounts = get_fixed_discounts()
    query = get_query()
    results = []
    for discount in db_fixed_discounts.search(query.deleted == False):
        result = {}
        result['id'] = discount.doc_id
        result['description'] = discount['description']
        if discount['calculated_in'] == 'value':
            result['value'] = format_currency(
                discount['value'], get_user_config().get(doc_id=1)['currency']
            )
        else:
            result['value'] = format_percent(
                discount['value'] / 100,
                locale=get_locale(),
                decimal_quantization=False,
            )
        results.append(result)
    return {'fixed_discounts': results}, 200


@api.route('/fixed-discount', methods=['POST'])
def post_fixed_discount():
    data = request.get_json()
    data['deleted'] = False
    db_fixed_discounts = get_fixed_discounts()
    db_fixed_discounts.insert(data)
    return {'message': _('Fixed discount successfully registered!')}, 201


@api.route('/fixed-discount/<int:id>', methods=['DELETE'])
def delete_fixed_discount(id):
    db_fixed_discounts = get_fixed_discounts()
    data = db_fixed_discounts.get(doc_id=id)
    data['deleted'] = True
    db_fixed_discounts.update(data, doc_ids=[id])
    return {'message': _('Fixed discount successfully deleted!')}, 200
