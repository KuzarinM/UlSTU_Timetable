from bs4 import BeautifulSoup

import EEPROM
from Subject import Subject
from Settings import *
import aiosqlite
import asyncio


def get_teacher_name(soup):
    # Метод вытаскивает имя учителя и текущую неделю из заголовка станицы

    info = soup.body.find_all('font')[1].contents
    name = info[0][1:-1]  # Имя, но без первого и последнего символа(там вроде ак мусор какой-то или пробелы)
    week = info[2][info[2].find(": ") + 2:].replace("-я", "")  # Неделя опять таки тербует очистки от буковки
    return name, int(week)  # Неделю переводим в число


async def timetable_analise(soup, connection, updetes):
    # Метод обрабатывающий расписание учителя по неделям

    teacher, week = get_teacher_name(soup)  # Вытаскиваем имя учителя и номер текущей недели
    teacher = await test_entities(connection, "teacher", teacher)  # Вытаскиваем id (если надо, добавляем учителя в БД)
    tables = soup.body.find_all("table")  # Вытаскиваем из станицы только таблицы(2 недели)
    # Парсим распиание недели для учителя с id по неделе указанной выше
    await table_parse(tables[0].find_all("tr"), connection, teacher, week, updetes)
    if len(tables) > 1:  # не всегда есть вторая неделя(например в начала семестра). Так что тестим
        await table_parse(tables[1].find_all("tr"), connection, teacher, week + 1, updetes)


async def table_parse(lines, connection, teacher, week, updates):
    # Непосредственно парсим распиание из таблицы

    for i in range(2, len(lines)):  # проходится по строкам
        column = lines[i].find_all("td")  # получаем строку(ага, в названии косяк. Потом поправлю)
        for j in range(1, len(column)):  # Получаем элементы строки
            content = column[j].contents[1].contents[0].contents  # Непосредственно содержимое ячейки таблицы
            # А вот тут косяк источника. Там отсутствие пар бывает или как "-" или как " " или как "_"
            if content[0] != "-" and content[0] != ' ' and content[0] != '_' and len(content) > 4:
                sub = Subject(teacher, content, [i - 2, j - 1],
                              week)  # формируем запись о занятии. Класс работает как обёртка
                await check_subject(connection, sub,
                                    updates)  # Отдельный метод для проверки  обновления сведений о занятиях в БД


async def test_entities(conn, entities, name):
    # Универсальный метод для проверки наличия в БД сущностей(учителя, группы, дисциплины)
    # Общая логика работы:
    # 1 создаём курсор.
    # 2 Пробуем сделать SELECT запрос для доступа к сущности(имя = entities) по имени(name)
    # 3 Получаем ответ в переменную one_result. Проверяем, равно ли None:
    #       4.1 Если равно, то коммитим в БД и возвращаем id сущности
    #       4.2 Если нет, то вызываем команду INSERT(создаём сущность новую). Делаем шаг 2. Далее делаем шаг 4.1

    cur = await conn.cursor()
    await cur.execute(sql_select_from_entities(entities, name))
    one_result = await cur.fetchone()
    if one_result is None:
        await cur.execute(sql_insert_into_entities(entities, name))
        await cur.execute(sql_select_from_entities(entities, name))
        one_result = await cur.fetchone()
    await conn.commit()
    return one_result[0]  # возвращаем id


async def set_subject(conn, subject, gid, updates):
    # Основной метод создания и обновления сведений о занятии Его логика работы схожа с логикой работы метода
    # test_entities, однако отличие в кол-ве данных(тут не только навзание) но и положение на неделе, группа,
    # дисциплина, аудитория и т п. Так же есть 1 новый механизм: если в БД уже есть точно таккая же запись,
    # то нужно обновить прзнак модификации на 0. Если создаём новую запись - признак модификации 1

    cur = await conn.cursor()
    print(sql_select_from_subject(subject, gid))
    await cur.execute(sql_select_from_subject(subject, gid))
    one_result = await cur.fetchone()
    if one_result is None:
        await cur.execute(sql_insert_into_subject(subject, gid))
        await cur.execute(sql_select_from_subject(subject, gid))
        one_result = await cur.fetchone()
    else:
        updates.append({"gid": gid, "tid": subject.teacher_id})  # добавляем в массив обновлённых данных
        await cur.execute(sql_update_subject(subject, gid))
    await conn.commit()
    # Фактически возвращать ничего не нужно, но на всякий случай и для сохранения общего стилая тут Id врнётся
    return one_result[0]


async def check_subject(conn, subject, updates):
    # Подготовка данных для запуска систмы добавлни/обовления занятия в БД

    subject.discipline_id = await test_entities(conn, "Discipline",
                                                subject.name)  # Получаем Id дисциплины(если надо создаём)
    for i in subject.groups:  # Проходимся по группам
        group = await test_entities(conn, "group", i)  # Получаем id грппы(если надо - содаём)
        await set_subject(conn, subject, group,
                          updates)  # Вызываем метод создания/обновления занятия для конкретной группы.


async def open_file(id, conn, err, updates):
    # Метод открывает конкретный файл из Data/<tid>.html и вытаскивает из него данные (html код)

    with open(f"{html_save_path}{id}.html", "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')  # С помощью библиотеки работать с html проще
        # Так как в процессе работы могут возникать ошибки(мло ли), то этот блок их будет ловить
        await timetable_analise(soup, conn, updates)  # Основной метод обработки информации учителя


async def operate():
    # Основной метод для запуска обновления БД. Все остальные запускаются отсюда

    conn = await aiosqlite.connect(db_path)  # создаём подключение к БД
    # Блок отвечающий за удаление неактуальной информации и обновление статусов
    cur = await conn.cursor()  # Создаём курсор
    await cur.execute(clear_old_sql_request)  # Удаляем все старые данные(в прошлый раз не были подтверждеы)
    await cur.execute(set_unchecked_mode_sql_request)  # Ставим всем записям статус неактуальные
    await conn.commit()

    errors = []  # Лист из id тех учителей, при обработке который вышла ошибка
    updates = []  # По идеи, список всех обновлённых id(там картеж)
    teachers_count = EEPROM.read_data("teachers_count")  # Получаем из файла настроек текущее колличество учителей
    for i in range(1, teachers_count):
        print("обработка расписания преподавателя " + str(i))
        await open_file(i, conn, errors, updates)  # Основной метод обработки
    print(f"Ошибки в обработке:{errors}")
    print("Было обновлено:")
    print(*updates, sep="\n")
    await conn.close()  # Освобождаем ресурсы => асинхронная функция завершается


if __name__ == '__main__':
    # Имнно так и нужно запускать данный модуль из вне. Через asyncio
    asyncio.run(operate())
