from flask import Blueprint, render_template
from flaskwebgui import close_application

from abaco.constants import APP_NAME
from abaco.database import database_exists

web = Blueprint('web', __name__)


@web.route('/')
def hello():

    if not database_exists():

        data = {'title': 'Welcome! | ' + APP_NAME}
        return render_template('welcome.html', data=data)

    return render_template('index.html')


@web.route('/close', methods=['GET'])
def close_window():
    close_application()
