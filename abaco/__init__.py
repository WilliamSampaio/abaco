import os

from flask import Flask

from abaco import localization
from abaco.blueprints import api, web
from abaco.constants import APP_ENV, APP_NAME

base_dir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    if APP_ENV == 'development':
        app.config['APP_NAME'] = APP_NAME + ' (Dev)'
    else:
        app.config['APP_NAME'] = APP_NAME
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(
        base_dir, 'translations'
    )
    localization.init_app(app)
    api.init_app(app)
    web.init_app(app)
    return app


app = create_app()
