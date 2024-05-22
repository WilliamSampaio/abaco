import os

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
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


engine = db.create_engine(get_database_uri())
Session = sessionmaker(bind=engine)


def get_database_conn():
    return engine.connect()


def database_exists():
    return os.path.exists(db_path_cache)


def get_db() -> TinyDB:
    if not os.path.exists(dir):
        os.makedirs(dir)
    return TinyDB(db_path_cache)


def get_table(table_name: str, db_instance: TinyDB) -> TinyDB:
    db_instance.default_table_name = table_name
    return db_instance


def get_stocks() -> TinyDB:
    return get_table('stocks', get_db())


def get_query():
    return Query()
