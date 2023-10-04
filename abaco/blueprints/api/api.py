import json
from io import BytesIO

from flask import Blueprint, request
from flask_babel import gettext as _

from abaco.database import db_filename, get_user_config, validate_schema
from abaco.utils import validate_json

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/newapp', methods=['POST'])
def newapp():
    data = request.get_json()
    db_user_config = get_user_config()
    db_user_config.insert(data)
    return {'message': _('Abaco created successfully')}, 201


@api.route('/importdatabase', methods=['POST'])
def importdatabase():
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


@api.route('/settings', methods=['POST'])
def settings():
    data = request.get_json()
    db_user_config = get_user_config()
    db_user_config.update(data)
    return {}, 200
