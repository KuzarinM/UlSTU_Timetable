from Subject import Subject

# HTML
html_header = "<HTML>\n" \
              "<HEAD>\n" \
              "<TITLE>Расписание.net</TITLE>\n" \
              "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n" \
              "</HEAD>\n" \
              "<BODY style=\"background: white;\">\n"
template = "<TABLE border=\"#000000\" cellspacing=\"3\" STYLE=\"width:90%\">\n" \
           "<thead>\n" \
           "<tr>\n" \
           "<td><P ALIGN=\"CENTER\">Пары</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">1-я</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">2-я</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">3-я</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">4-я</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">5-я</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">6-я</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">7-я</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">8-я</p> </td>\n" \
           "</tr>\n" \
           "<tr>\n" \
           "<td><P ALIGN=\"CENTER\">Время</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">08:30-09:50</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">10:00-11:20</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">11:30-12:50</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">13:30-14:50</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">15:00-16:20</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">16:30-17:50</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">18:00-19:20</p></td>\n" \
           "<td><P ALIGN=\"CENTER\">19:30-20:50</p></td>\n" \
           "</tr>\n" \
           "</thead>\n" \
           "<tbody>\n"
# SQL запросы
data_sql_request = "SELECT subject.week, subject.dayofweak, subject.pairnumber, subject.type, discipline.name dname, " \
                   "teacher.name tname, subject.isdifference, subject.place FROM subject join discipline ON " \
                   "discipline.id = subject.disciplineid Join teacher ON teacher.id = subject.teacherid " \
                   "WHERE subject.groupId="
group_sql_request = "SELECT * FROM \"group\" WHERE name="
clear_old_sql_request ="DELETE FROM subject WHERE isdifference=1"
set_unchecked_mode_sql_request = "UPDATE subject set isdifference = 1"
# Константы файла
db_path = "Univercity.db"
res_html_path = "resout.html"
res_jpg_path = "resout.jpg"
html_save_path = "Data/"
# Константы работы
teachers_count = 603
username = "m.kuzyarin"
session = "okc6chlbqqmii3sg318clj2fc8"
types = {"лек": "Лекция:", "пр": "Практика:", "лаб": "Лабораторка:"}
days = ["Пнд.", "Втр.", "Срд.", "Чтв.", "Птн.", "Сбт."]
#URL запросов
timetable_url = "https://lk.ulstu.ru/timetable/shared/teachers/m"
#Глобальные переменные
global_timetable = []

# Сложные SQL запросы
def sql_insert_into_subject(subject, group_id):
    return f"INSERT INTO Subject " \
           f"(disciplineid, teacherid, groupid, type, dayofweak, pairnumber, week, isdifference, place) " \
           f"VALUES({subject.discipline_id}, {subject.teacher_id}, {group_id}, '{subject.type}', " \
           f"{subject.day}, {subject.pair}, {subject.week}, 2, '{subject.place}')"


def sql_select_from_subject(subject, group_id):
    return f"SELECT * FROM Subject WHERE " \
           f"disciplineid={subject.discipline_id} " \
           f"AND teacherid={subject.teacher_id} " \
           f"AND groupid={group_id} " \
           f"AND dayofweak={subject.day} " \
           f"AND pairnumber={subject.pair} " \
           f"AND week={subject.week} " \
           f"AND place='{subject.place}'"


def sql_update_subject(subject, group_id):
    return f"UPDATE Subject SET isdifference=0 WHERE" \
           f" disciplineid={subject.discipline_id} " \
           f"AND teacherid={subject.teacher_id} " \
           f"AND groupid={group_id} " \
           f"AND dayofweak={subject.day} " \
           f"AND pairnumber={subject.pair} " \
           f"AND week={subject.week}"


def sql_select_from_entities(entities_name, object_name):
    return f"SELECT * FROM \"{entities_name}\" WHERE name = '{object_name}'"


def sql_insert_into_entities(entities_name, object_name):
    return f"INSERT INTO \"{entities_name}\" (name) VALUES ('{object_name}')"