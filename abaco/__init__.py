import os

from dynaconf import FlaskDynaconf
from flask import Flask

base_dir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    FlaskDynaconf(
        app=app,
        extensions_list='EXTENSIONS',
    )
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(
        base_dir, 'translations'
    )
    return app
