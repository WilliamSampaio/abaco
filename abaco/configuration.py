from dynaconf import Dynaconf, FlaskDynaconf

settings = Dynaconf(settings_file='settings.toml', environments=True)


def init_app(app):
    FlaskDynaconf(
        app=app, dynaconf_instance=settings, extensions_list='EXTENSIONS'
    )
