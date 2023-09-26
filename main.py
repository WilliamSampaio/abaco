import os

from tinydb import TinyDB

# import pathlib
from config import settings

if __name__ == '__main__':

    data_folder = settings.data_folder
    explain_json_format = settings.explain_json_format

    if not os.path.exists(os.path.join(os.getcwd(), data_folder)):
        os.mkdir(os.path.join(os.getcwd(), data_folder))

    db_filename = os.path.join(
        os.getcwd(),
        data_folder,
        (
            os.environ.get('USER')
            + '.abaco'
            + ('.json' if explain_json_format is True else '')
        ),
    )

    # if not pathlib.Path.is_file(db_filename):
    db = TinyDB(db_filename)
    db.default_table_name = 'teste_eilliam'

    db.insert(
        {'user_config': {'name': 'William Sampaio', 'language': 'pt-BR'}}
    )
