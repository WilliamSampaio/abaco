from locale import getdefaultlocale

from babel.numbers import format_percent as fp
from flask import g
from flask_babel import Babel
from flask_babel import format_currency as fc

from abaco.database import empty_user_config, get_user_config
from abaco.models import UserConfig


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


def format_currency(value: float):
    return fc(value, UserConfig().find(1).currency)


def format_percent(value: float):
    return fp(value / 100, locale=get_locale(), decimal_quantization=False)


def init_app(app):
    Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)
