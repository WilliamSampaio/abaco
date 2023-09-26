from .web import web


def init_app(app):
    app.register_blueprint(web)
