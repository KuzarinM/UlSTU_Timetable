import json
import os

import Settings
from Settings import *


def create_settings_json():
    if not os.path.exists("settings.json"):
        with open("settings.json", "w") as f:
            json.dump({
                "version": 1.1,
                "last_update": "0|0|0|0|0",
                "password": "",
                "api_key": "28022023",
                "teachers_count": 602
                }, f)
    if not os.path.exists("Data"):
        os.mkdir("Data")


def read_data(key):
    with open("settings.json", "r") as f:
        data = dict(json.load(f))
        if data["version"] < Settings.current_setiings_version:
            raise ValueError("Версия settings.json ниже требуемой. Пересоздайте файл")
        if key in data:
            return data[key]
    return None


def write_data(key, value):
    data = dict()
    with open("settings.json", "r") as f:
        data = dict(json.load(f))
        if data["version"] < Settings.current_setiings_version:
            raise ValueError("Версия settings.json ниже требуемой. Пересоздайте файл")
    data[key] = value
    with open("settings.json", "w") as f:
        json.dump(data, f)


def read_all():
    with open("settings.json", "r") as f:
        data = dict(json.load(f))
        if data["version"] < Settings.current_setiings_version:
            raise ValueError("Версия settings.json ниже требуемой. Пересоздайте файл")
        return data
