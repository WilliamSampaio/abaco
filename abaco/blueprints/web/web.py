from flask import Blueprint, render_template
from flask_babel import gettext as _
from flaskwebgui import close_application

from abaco.constants import COUNTRIES, CURRENCIES
from abaco.database import database_exists, empty_user_config, get_user_config

web = Blueprint('web', __name__)


@web.route('/')
def index():

    if not database_exists() or empty_user_config():

        data = {
            'title': _('Welcome!'),
            'countries': COUNTRIES,
            'currencies': CURRENCIES,
        }
        return render_template('welcome.html.jinja', data=data)

    data = {
        'user_config': get_user_config().all()[0],
        'title': _('Home'),
        'countries': COUNTRIES,
        'currencies': CURRENCIES,
    }
    return render_template('index.html.jinja', data=data)


@web.route('/exit', methods=['GET'])
def close_window():
    close_application()


@web.route('/hello', methods=['GET'])
def hello():
    return render_template('hello.html.jinja', data={'title': 'Hello!'})
