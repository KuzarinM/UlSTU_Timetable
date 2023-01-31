import datetime
import asyncio
from time import sleep
from DownloadTools import download
from DatabaseEditor import operate
from UserInterface import get_data


def CheckTime(lastUpdate):
    last = datetime.datetime(int(lastUpdate[0]), int(lastUpdate[1]), int(lastUpdate[2]),
                             int(lastUpdate[3]), int(lastUpdate[4]))
    diff = (datetime.datetime.now() - last).total_seconds()
    print("С момента обновления прошло: "+str(diff))
    if (diff < 3600):
        return False
    return True


def ReadEEPROM():
    needUpdate = True
    with open("settings.txt", "r") as f:
        setting = f.read()
        setting = setting.split("\n")
        needUpdate = CheckTime(setting[0].split("|"))
    return needUpdate


def WriteEEPROM():
    with open("settings.txt", "w") as f:
        setting = datetime.datetime.now().strftime("%Y|%m|%d|%H|%M") + "\n"
        f.write(setting)


if __name__ == '__main__':
    Groupe = "ПИбд-23"
    needUpdate = ReadEEPROM()
    if(needUpdate):
        download()
        WriteEEPROM()
    sleep(5)
    asyncio.run(operate())





