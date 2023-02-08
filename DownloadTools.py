# -*- coding: utf-8 -*-
from requests import request
from Settings import *
from time import sleep
import os

def get_URL(i):
    return timetable_url + str(i) + ".html"


def normalise_HTML(html):
    html = html.replace("</br>", "<br>")
    html = html.replace(".", "")
    return html


def get_HTML(id):
    global session
    for i in range(100):
        try:
            sleep(0.3)
            res = request('GET', get_URL(id), cookies={"AMS_LAST_LOGIN": username, "AMS_SESSION_ID": session})
            if res.status_code != 200:
                sleep(2)
                print(f"код{res.status_code} на позиции {id} всего{i + 1}")
                continue
            return res
        except Exception:
            sleep(2)
            print(f"остановка на позиции {id} всего{i + 1}")
    return None


def download(password):
    #authentication(username, password)
    for i in range(1, teachers_count):
        data = get_HTML(i)
        if data is not None:
            data = normalise_HTML(data.content.decode('cp1251'))
            if os.path.exists(f"{html_save_path}{str(i)}.html"):
                with open(f"{html_save_path}{str(i)}.html", "r") as last:
                    last_html = last.read()
                    last_html = last_html[last_html.find("<BODY>"):last_html.find("</BODY>")]

                    new_html = data[data.find("<BODY>"):data.find("</BODY>")]
                    new_html = new_html.replace("\r", "\n")

                    if last_html != new_html:
                        with open(f"{html_save_path}{str(i)}.html", "w") as f:
                            f.write(data)
                            print(f"Страница {str(i)} была изменена!")
                    else:
                        print(f"Страница {str(i)}")
            else:
                with open(f"{html_save_path}{str(i)}.html", "w") as f:
                    f.write(data)
                    print(f"Страница {str(i)} была создана!")


def authentication(login, password):
    global session
    response = request("POST", authentication_url, data={"login": login, "password": password})
    if response.status_code == 200:
        session_id = response.history[0].cookies.get("AMS_SESSION_ID")
        if session_id is not None:
            session = session_id
            return session
    return False


if __name__ == '__main__':
    download("")
