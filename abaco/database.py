import os

db_filename = os.path.join(
    os.environ.get('HOME'), '.abaco', 'database.abaco.json'
)


def database_exists():
    return os.path.exists(db_filename)


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
