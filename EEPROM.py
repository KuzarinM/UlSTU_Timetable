import json
from Settings import *


def create_settings_json():
    with open("settings.json", "w") as f:
        json.dump({"version": 1.0, "last_update": "0|0|0|0|0", "password": "", "api_key": "28022023"}, f)


def read_data(key):
    with open("settings.json", "r") as f:
        data = dict(json.load(f))
        if key in data:
            return data[key]
    return None


def write_data(key, value):
    data = dict()
    with open("settings.json", "r") as f:
        data = dict(json.load(f))
    data[key] = value
    with open("settings.json", "w") as f:
        json.dump(data, f)


def read_all():
    with open("settings.json", "r") as f:
        return dict(json.load(f))
