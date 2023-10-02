from locale import getdefaultlocale

from flask import g
from flask_babel import Babel

from abaco.database import get_user_config


def get_locale():
    user_configs = get_user_config().all()
    if len(user_configs) == 0:
        return getdefaultlocale()[0]
    user_config = user_configs[0]
    if 'language' not in user_config or user_config['language'] == '':
        return getdefaultlocale()[0]
    return user_config['language']


def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


def init_app(app):
    Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)
