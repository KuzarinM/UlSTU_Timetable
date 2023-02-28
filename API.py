# -*- coding: utf-8 -*-
import sqlite3
from Settings import *
from UserInterface import create_HTML, get_data
import EEPROM
import main
from flask import Flask
from flask import jsonify, request

app = Flask(__name__)


def key_test(key):
    need_key = EEPROM.read_data("api_key")
    if key == need_key:
        return True
    return False


def field_naming(data, names):
    resout = []
    for element in data:
        item = {}
        for i in range(len(names)):
            item[names[i]] = element[i]
        resout.append(item)
    return resout


def try_get_first(data):
    if len(data) == 0:
        return None
    return data[0]


def create_subject_params(args):
    resout = "WHERE "
    flag = False
    if args.get("did") is not None:
        if flag:
            resout += "AND"
        else:
            flag = True
        resout += f" disciplineid={args.get('did')} "
    if args.get("tid") is not None:
        if flag:
            resout += "AND"
        else:
            flag = True
        resout += f" teacherid={args.get('tid')} "
    if args.get("gid") is not None:
        if flag:
            resout += "AND"
        else:
            flag = True
        resout += f" groupid={args.get('gid')} "
    if args.get("w") is not None:
        if flag:
            resout += "AND"
        else:
            flag = True
        resout += f" week={args.get('w')} "
    if args.get("d") is not None:
        if flag:
            resout += "AND"
        else:
            flag = True
        resout += f" dayofweak={args.get('d')} "
    if args.get("pn") is not None:
        if flag:
            resout += "AND"
        else:
            flag = True
        resout += f" pairnumber={args.get('pn')} "
    if args.get("pl") is not None:
        if flag:
            resout += "AND"
        else:
            flag = True
        resout += f" place='{args.get('pl')}' "
    if args.get("m") is not None:
        if flag:
            resout += "AND"
        else:
            flag = True
        resout += f" isdifference={args.get('m')} "
    return resout


def to_standard(text):
    return text[0].upper() + text[1:]


@app.route('/api/<string:key>/groups', methods=['GET'])
def groups(key):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute('SELECT * FROM "group"')
    resouts = field_naming(cur.fetchall(), ["id", "name"])
    return jsonify(resouts)


@app.route('/api/<string:key>/group/<int:id>', methods=['GET'])
def group_id(key, id):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute(f'SELECT * FROM "group" WHERE id={id}')
    resouts = field_naming(cur.fetchall(), ["id", "name"])
    return jsonify(try_get_first(resouts))


@app.route('/api/<string:key>/group/<string:name>', methods=['GET'])
def group_name(key, name):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute(f'SELECT * FROM "group" WHERE name=\'{name}\'')
    resouts = field_naming(cur.fetchall(), ["id", "name"])
    return jsonify(try_get_first(resouts))


@app.route('/api/<string:key>/teachers', methods=['GET'])
def teachers(key):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute('SELECT * FROM teacher')
    resouts = field_naming(cur.fetchall(), ["id", "name"])
    return jsonify(resouts)


@app.route('/api/<string:key>/teacher/<int:id>', methods=['GET'])
def teacher_id(key, id):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute(f'SELECT * FROM teacher WHERE id={id}')
    resouts = field_naming(cur.fetchall(), ["id", "name"])
    return jsonify(try_get_first(resouts))


@app.route('/api/<string:key>/teacher/<string:name>', methods=['GET'])
def teacher_name(key, name):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute(f'SELECT * FROM teacher WHERE name=\'{name}\'')
    resouts = field_naming(cur.fetchall(), ["id", "name"])
    return jsonify(try_get_first(resouts))


@app.route('/api/<string:key>/disciplines', methods=['GET'])
def disciplines(key):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute('SELECT * FROM discipline')
    resouts = field_naming(cur.fetchall(), ["id", "name"])
    return jsonify(resouts)


@app.route('/api/<string:key>/discipline/<int:id>', methods=['GET'])
def discipline_id(key, id):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute(f'SELECT * FROM discipline WHERE id={id}')
    resouts = field_naming(cur.fetchall(), ["id", "name"])
    return jsonify(try_get_first(resouts))


@app.route('/api/<string:key>/discipline/<string:name>', methods=['GET'])
def discipline_name(key, name):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute(f'SELECT * FROM discipline WHERE name=\'{name}\'')
    resouts = field_naming(cur.fetchall(), ["id", "name"])
    return jsonify(try_get_first(resouts))


@app.route('/api/<string:key>/subjects', methods=['GET'])
def subjects(key):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute('SELECT * FROM subject')
    resouts = field_naming(cur.fetchall(), ["id", "disciplineId", "teacherId", "groupId", "type",
                                            "day", "pair", "week", "diference", "place"])
    return jsonify(resouts)


@app.route('/api/<string:key>/subject/<int:id>', methods=['GET'])
def subject_id(key, id):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute(f'SELECT * FROM subject WHERE id={id}')
    resouts = field_naming(cur.fetchall(), ["id", "disciplineId", "teacherId", "groupId", "type",
                                            "day", "pair", "week", "diference", "place"])
    return jsonify(try_get_first(resouts))


@app.route('/api/<string:key>/subject', methods=['GET'])
def subject(key):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute(f'SELECT * FROM subject {create_subject_params(request.args)}')
    resouts = field_naming(cur.fetchall(), ["id", "disciplineId", "teacherId", "groupId", "type",
                                            "day", "pair", "week", "diference", "place"])
    return jsonify(resouts)


@app.route('/api/<string:key>/timetable/<int:gid>', methods=['GET'])
def timetable(key, gid):
    if not key_test(key):
        return "Ключ не верен"
    db_connection = sqlite3.connect(db_path)
    cur = db_connection.cursor()
    cur.execute(data_sql_request + str(gid))
    data = cur.fetchall()
    timetable = [[[[] for j in range(0, 9)] for i in range(0, 6)] for k in range(0, 2)]
    for record in data:
        output = [record[3], to_standard(record[4]), record[5], record[6], record[7]]
        output = field_naming([output], ["type", "dname", "tname", "modifired", "place"])
        timetable[record[0]][record[1]][record[2]].append(*output)
    return jsonify(timetable)


@app.route('/timetable/<string:group>')
def user_timetable(group):
    timetable = get_data(group)
    return create_HTML(timetable, group)


@app.route('/api/<string:key>/db/update')
def db_update(key):
    if not key_test(key):
        return "Ключ не верен"
    lgn = request.args.get("login")
    psw = request.args.get("password")
    if lgn is None:
        return "Укажите логин через парамметр login"
    if psw is None:
        return "Укажите пароль через парамметр password"
    main.update(lgn, psw)
    return "Процедура обновления завершена."

@app.route('/api/<string:key>/db/update-status')
def db_status(key):
    global in_updating
    if not key_test(key):
        return "Ключ не верен"
    if in_updating:
        return "База данных обновляется"
    return "Штатное функционирование"



if __name__ == '__main__':
    app.run(debug=True)
