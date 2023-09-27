from flask import Blueprint, render_template
from flaskwebgui import close_application

from abaco.constants import APP_NAME
from abaco.database import database_exists, get_user_config

web = Blueprint('web', __name__)


@web.route('/')
def hello():

    if not database_exists():

        data = {'title': 'Welcome! | ' + APP_NAME}
        return render_template('welcome.html', data=data)

    data = get_user_config().all()[0]
    print(data)
    data['title'] = APP_NAME
    return render_template('index.html', data=data)


@web.route('/exit', methods=['GET'])
def close_window():
    close_application()
