import os

from tinydb import Query, TinyDB

from .config import settings

db_filename_wallets = 'wallets.abaco'
db_filename_cache = 'cache.abaco.json'

if settings.ENV_FOR_DYNACONF == 'DEVELOPMENT':
    dir = os.getcwd()
    db_path_cache = os.path.join(dir, db_filename_cache)
elif settings.ENV_FOR_DYNACONF == 'PRODUCTION':
    dir = os.path.join(os.environ.get('HOME'), '.abaco')
    db_path_cache = os.path.join(dir, db_filename_cache)


def get_database_uri() -> str:
    return settings.SQLALCHEMY_DATABASE_URI.format(
        dir,
        db_filename_wallets,
    )


def database_exists():
    return os.path.exists(db_path_cache)


def get_db() -> TinyDB:
    if not os.path.exists(dir):
        os.makedirs(dir)
    return TinyDB(db_path_cache)


def get_table(table_name: str, db_instance: TinyDB) -> TinyDB:
    db_instance.default_table_name = table_name
    return db_instance


def get_user_config() -> TinyDB:
    return get_table('user_config', get_db())


def get_fixed_discounts() -> TinyDB:
    return get_table('fixed_discounts', get_db())


def empty_user_config():
    if len(get_user_config().all()) == 0:
        return True
    return False


def get_query():
    return Query()
