from locale import getdefaultlocale

from flask import g
from flask_babel import Babel

from abaco.database import get_user_config


def get_locale():
    if len(get_user_config().all()) == 0:
        return getdefaultlocale()[0]
    return get_user_config().all()[0]['language']


def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


def init_app(app):
    Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)
