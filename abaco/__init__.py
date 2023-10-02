import os

from flask import Flask

from abaco import configuration

base_dir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(
        base_dir, 'translations'
    )
    configuration.init_app(app)
    return app


app = create_app()
