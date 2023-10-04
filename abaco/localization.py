from locale import getdefaultlocale

from flask import g
from flask_babel import Babel

from abaco.database import empty_user_config, get_user_config


def get_locale():
    if empty_user_config():
        return getdefaultlocale()[0]
    user_config = get_user_config().all()[0]
    if 'language' not in user_config or user_config['language'] == '':
        return getdefaultlocale()[0]
    return user_config['language']


def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


def init_app(app):
    Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)
