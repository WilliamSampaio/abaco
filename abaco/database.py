import json
import os

from schema import And, Schema
from tinydb import Query, TinyDB

from abaco.constants import APP_ENV

db_filename = 'database.abaco.json'

if APP_ENV == 'development':
    dir = os.getcwd()
    db_path = os.path.join(dir, db_filename)
elif APP_ENV == 'production':
    dir = os.path.join(os.environ.get('HOME'), '.abaco')
    db_path = os.path.join(dir, db_filename)


def database_exists():
    return os.path.exists(db_path)


def get_db() -> TinyDB:
    if not os.path.exists(dir):
        os.makedirs(dir)
    return TinyDB(db_path)


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


def validate_schema(schema: dict):
    base_dir = os.path.abspath(os.path.dirname(__file__))

    def for_over_dict(dictionary: dict):
        for key, value in dictionary.items():
            if type(dictionary[key]) == dict:
                dictionary[key] = for_over_dict(dictionary[key])
                continue
            if type(value) == str:
                dictionary[key] = And(str)
                continue
            if type(value) == float:
                dictionary[key] = And(float)
                continue
            if type(value) == int:
                dictionary[key] = And(int)
                continue
            if type(value) == bool:
                dictionary[key] = And(bool)
                continue
        return dictionary

    f = open(os.path.join(base_dir, 'schemas', 'database.json'))
    valid_schema = json.load(f)
    for table in schema.keys():
        try:
            valid_row = Schema(for_over_dict(valid_schema[table]['1']))
        except:
            return False
        for key in dict(schema[table]).keys():
            try:
                valid_row.validate(schema[table][key])
            except:
                return False
    return True
