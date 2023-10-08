import os
import zipfile
from datetime import datetime
from pathlib import Path

from flask import Blueprint, render_template, send_file
from flask_babel import gettext as _
from flaskwebgui import close_application

from abaco.configuration import settings
from abaco.constants import BASE_DIR_TEMP, COUNTRIES, CURRENCIES
from abaco.database import database_exists, db_path, empty_user_config
from abaco.localization import get_locale
from abaco.models import FixedDiscount, UserConfig
from abaco.utils import populate_fake_db, purge_temp_files

web = Blueprint('web', __name__)


@web.route('/')
def index():

    lang = get_locale().replace('_', '-')

    if not database_exists() or empty_user_config():

        if settings['APP_ENV'] == 'development':

            if populate_fake_db():
                data = {
                    'lang': lang,
                    'initial_date': datetime.today().strftime('%Y-%m-01'),
                    'final_date': datetime.today().strftime('%Y-%m-%d'),
                    'user_config': UserConfig().find(1).as_dict(),
                    'fixed_discounts': FixedDiscount().available(),
                    'title': _('Home'),
                    'countries': COUNTRIES,
                    'currencies': CURRENCIES,
                }
                return render_template('index.html.jinja', data=data)

        data = {
            'lang': lang,
            'title': _('Welcome!'),
            'countries': COUNTRIES,
            'currencies': CURRENCIES,
        }
        return render_template('welcome.html.jinja', data=data)

    data = {
        'lang': lang,
        'initial_date': datetime.today().strftime('%Y-%m-01'),
        'final_date': datetime.today().strftime('%Y-%m-%d'),
        'user_config': UserConfig().find(1).as_dict(),
        'fixed_discounts': FixedDiscount().available(),
        'title': _('Home'),
        'countries': COUNTRIES,
        'currencies': CURRENCIES,
    }
    return render_template('index.html.jinja', data=data)


@web.route('/backup', methods=['GET'])
def backup():
    if os.path.exists(db_path):
        if not os.path.exists(BASE_DIR_TEMP):
            os.mkdir(BASE_DIR_TEMP)
        output_filename = os.path.join(
            BASE_DIR_TEMP,
            datetime.now().strftime('abaco_%Y-%m-%d_%H-%M-%S.zip'),
        )
        with zipfile.ZipFile(output_filename, mode='w') as zip:
            zip.write(db_path, Path(db_path).name)
        return send_file(output_filename, mimetype='application/zip')


@web.route('/exit', methods=['GET'])
def close_window():
    purge_temp_files()
    close_application()


@web.route('/hello', methods=['GET'])
def hello():

    lang = get_locale().replace('_', '-')

    return render_template(
        'hello.html.jinja', data={'lang': lang, 'title': 'Hello!'}
    )
