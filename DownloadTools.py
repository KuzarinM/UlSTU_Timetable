# -*- coding: utf-8 -*-
from requests import request
from requests import Session
from Settings import *
from time import sleep
import os

def get_URL(i):
    return timetable_url + str(i) + ".html"


def normalise_HTML(html):
    html = html.replace("</br>", "<br>")
    html = html.replace(".", "")
    return html


def get_HTML(id, ses):
    global session_id
    for i in range(100):
        try:
            sleep(0.2)
            #на случай, если появится желание использовать session_id
            res = ses.get(get_URL(id), cookies={"AMS_LAST_LOGIN": username, "AMS_SESSION_ID": session_id})
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
    my_session = authentication(username, password)
    for i in range(1, teachers_count):
        data = get_HTML(i,my_session)
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
    global session_id
    ses = Session()
    response = ses.post(authentication_url, data={"login": login, "password": password})
    if response.status_code == 200:
        ses_id =  response.history[0].cookies.get("AMS_SESSION_ID")
        if ses_id is not None:
            session_id = ses_id
            return ses
    return Session()



if __name__ == '__main__':
    download("")#пароль писсать сюда
