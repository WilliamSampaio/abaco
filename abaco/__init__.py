from flask import Flask

from abaco.blueprints import api, web

APP_NAME = 'Abaco'


def create_app():
    app = Flask(__name__)
    api.init_app(app)
    web.init_app(app)
    return app
