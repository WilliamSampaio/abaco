import json
from io import BytesIO

from flask import Blueprint, request

from abaco.database import db_filename, get_user_config
from abaco.utils import validate_json

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/newapp', methods=['POST'])
def newapp():
    data = request.get_json()
    db_user_config = get_user_config()
    db_user_config.insert(data)
    return data, 201


@api.route('/importdatabase', methods=['POST'])
def importdatabase():
    if 'database' not in request.files.keys():
        return {'message': 'Database file not sent'}, 400
    database = BytesIO(request.files.get('database').stream.read())
    # print(type(database.getvalue().decode()))
    # print(database.getvalue().decode())
    database_dict = None
    if validate_json(database.getvalue().decode()):
        database_dict = json.loads(database.getvalue().decode())
    else:
        return {'message': 'Database invalid'}, 400
    # print(type(database_dict))
    # print(database_dict)
    with open(db_filename, 'w') as database_file:
        database_file.write(json.dumps(database_dict))
    return {'message': 'Database imported successfully'}, 201
