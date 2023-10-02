import json
import os

from abaco.constants import BASE_DIR_TEMP


def validate_json(json_string: str):
    try:
        json.loads(json_string)
    except:
        return False
    return True


def purge_temp_files():
    for file in os.listdir(BASE_DIR_TEMP):
        os.remove(os.path.join(BASE_DIR_TEMP, file))
