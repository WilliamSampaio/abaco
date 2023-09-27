from flask import Flask

from abaco.blueprints import api, web


def create_app():
    app = Flask(__name__)
    api.init_app(app)
    web.init_app(app)
    return app
