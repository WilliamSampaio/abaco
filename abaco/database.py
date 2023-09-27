import os

from tinydb import TinyDB

db_filename = os.path.join(
    os.environ.get('HOME'), '.abaco', 'database.abaco.json'
)


def database_exists():
    return os.path.exists(db_filename)


def get_db() -> TinyDB:
    if not os.path.exists(os.path.join(os.environ.get('HOME'), '.abaco')):
        os.makedirs(os.path.join(os.environ.get('HOME'), '.abaco'))
    return TinyDB(db_filename)


def get_table(table_name: str, db_instance: TinyDB) -> TinyDB:
    db_instance.default_table_name = table_name
    return db_instance


def get_user_config() -> TinyDB:
    return get_table('user_config', get_db())


def empty_user_config():
    if len(get_user_config().all()) == 0:
        return True
    return False


# data_folder = settings.data_folder
#     explain_json_format = settings.explain_json_format

#     if not os.path.exists(os.path.join(os.getcwd(), data_folder)):
#         os.mkdir(os.path.join(os.getcwd(), data_folder))

#     db_filename = os.path.join(
#         os.getcwd(),
#         data_folder,
#         (
#             os.environ.get('USER')
#             + '.abaco'
#             + ('.json' if explain_json_format is True else '')
#         ),
#     )

#     # if not pathlib.Path.is_file(db_filename):
#     db = TinyDB(db_filename)
#     db.default_table_name = 'teste_eilliam'

#     db.insert(
#         {'user_config': {'name': 'William Sampaio', 'language': 'pt-BR'}}
#     )
