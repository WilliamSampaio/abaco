import json


def validate_json(json_string: str):
    try:
        json.loads(json_string)
    except:
        return False
    return True
