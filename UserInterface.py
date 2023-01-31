# -*- coding: utf-8 -*-
import sqlite3
from Settings import *
from html2image import Html2Image


def to_standard(text):
    return text[0].upper() + text[1:]


def get_data(group):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"{group_sql_request}'{group}'")
    one_result = cur.fetchone()
    if (one_result == None):
        print(f"Группа с таким названием как {group} не найдена")
        conn.commit()
        return
    gid = one_result[0]

    cur.execute(data_sql_request + str(gid))
    data = cur.fetchall()
    timetable = [[[[] for j in range(0, 9)] for i in range(0, 6)] for k in range(0, 2)]
    for record in data:
        timetable[record[0]][record[1]][record[2]].append([record[3], to_standard(record[4]), record[5], record[6],
                                                           record[7]])
    conn.commit()
    return timetable


def create_HTML(timetable, group):
    global global_timetable
    html = f"{html_header}<H1>Расписание для группы {group}</H1>\n<H2>Чётная неделя</H2>\n"
    html += template + create_table(timetable[0]) + "</tbody>\n</table>\n"
    html += "<H2>Нечётная неделя</H2>\n" + template + create_table(timetable[1])
    global_timetable = timetable
    return html


def create_table(timetable):
    html = ""
    for day in range(0, 6):
        html += f"<tr>\n<td><P ALIGN=\"CENTER\">{days[day]}</td>\n"
        for par in range(0, 8):
            color = "white"
            text = "-"

            if len(timetable[day][par]) != 0:
                text = ""
                for record in timetable[day][par]:
                    text += f"{types[record[0]]}<br>{record[1]}<br>{record[2]}<br>{record[4]}<br>"

                    if record[3] == 2:
                        color = "cyan"
                    elif record[3] == 1:
                        color = "brown"
                        text = "-"

            html += f"<td style=\"background-color: {color};\"><P ALIGN=\"CENTER\">{text}</p></td>\n"
        html += "</tr>\n"
    return html


def save_resout(text):
    with open(res_html_path, 'w') as f:
        f.write(text)


def create_jpg_version(timetable,group):
    hti = Html2Image()
    for i in range(2):
        info = "<H1>Чётная неделя</H1>\n"
        if i!=0 :
            info = "<H1>Нечётная неделя</H1>\n"
        html =html_header+info+template + create_table(timetable[i]) +"</tbody>\n</table>\n</HTML>\n</BODY>\n"
        hti.screenshot(html_str=html, save_as=f"{i+1}.jpg", size=(1200, 1000))


def create_html_version(timetable,group):
    save_resout(create_HTML(timetable, group))


if __name__ == '__main__':
    timetable = get_data("ПИбд-23")
    create_html_version(timetable,"ПИбд-23")
    create_jpg_version(timetable,"ПИбд-23")