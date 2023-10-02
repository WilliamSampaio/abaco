import json

from abaco.constants import BASE_DIR_TEMP


def validate_json(json_string: str):
    try:
        json.loads(json_string)
    except:
        return False
    return True


def purge_temp_files():
    print(BASE_DIR_TEMP)
