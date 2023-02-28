import datetime
import asyncio
from time import sleep
from DownloadTools import download
from DatabaseEditor import operate
import EEPROM
from Settings import *
from UserInterface import get_data


def check_time(last_update):
    last = datetime.datetime(int(last_update[0]), int(last_update[1]), int(last_update[2]),
                             int(last_update[3]), int(last_update[4]))
    diff = (datetime.datetime.now() - last).total_seconds()
    print("С момента обновления прошло: " + str(diff))
    return diff >= 3600


def initiate_update_sequence():
    global in_updating
    need_update = check_time(EEPROM.read_data("last_update").split("|"))
    in_updating = True
    if need_update:
        download(EEPROM.read_data("password"))
        EEPROM.write_data("last_update", datetime.datetime.now().strftime("%Y|%m|%d|%H|%M"))
    sleep(5)
    asyncio.run(operate())
    in_updating = False


def update(login, password):
    global in_updating
    in_updating = True
    download(password, login)
    sleep(5)
    asyncio.run(operate())
    in_updating = False



if __name__ == '__main__':
    initiate_update_sequence()
