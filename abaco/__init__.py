from flask import Flask

from abaco.blueprints import web


def create_app():
    app = Flask(__name__)
    web.init_app(app)
    return app
