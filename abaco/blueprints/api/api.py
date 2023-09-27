from flask import Blueprint, request

from abaco.database import get_user_config

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/newapp', methods=['POST'])
def newapp():
    data = request.get_json()
    db_user_config = get_user_config()
    db_user_config.insert(data)
    return data, 201
