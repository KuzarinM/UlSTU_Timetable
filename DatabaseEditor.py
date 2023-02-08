from bs4 import BeautifulSoup
from Subject import Subject
from Settings import *
import aiosqlite
import asyncio


def get_teacher_name(soup):
    info = soup.body.find_all('font')[1].contents
    name = info[0][1:-1]
    week = info[2][info[2].find(": ") + 2:].replace("-я", "")
    return name, int(week)


async def timetable_analise(soup, connection):
    teacher, week = get_teacher_name(soup)
    teacher = await test_entities(connection, "teacher", teacher)
    tables = soup.body.find_all("table")
    await table_parse(tables[0].find_all("tr"), connection, teacher, week)
    if len(tables) > 1:
        await table_parse(tables[1].find_all("tr"), connection, teacher, week + 1)


async def table_parse(lines, connection, teacher, week):
    for i in range(2, len(lines)):
        column = lines[i].find_all("td")
        for j in range(1, len(column)):
            content = column[j].contents[1].contents[0].contents
            if content[0] != "-" and content[0] != ' ' and content[0] != '_' and len(content) > 4:
                sub = Subject(teacher, content, [i - 2, j - 1], week)
                await check_subject(connection, sub)


async def test_entities(conn, entities, name):
    cur = await conn.cursor()
    await cur.execute(sql_select_from_entities(entities, name))
    one_result = await cur.fetchone()
    if one_result is None:
        await cur.execute(sql_insert_into_entities(entities, name))
        await cur.execute(sql_select_from_entities(entities, name))
        one_result = await cur.fetchone()
    await conn.commit()
    return one_result[0]


async def set_subject(conn, subject, gid):
    cur = await conn.cursor()
    await cur.execute(sql_select_from_subject(subject, gid))
    one_result = await cur.fetchone()
    if one_result is None:
        await cur.execute(sql_insert_into_subject(subject, gid))
        await cur.execute(sql_select_from_subject(subject, gid))
        one_result = await cur.fetchone()
    else:
        await cur.execute(sql_update_subject(subject, gid))
    await conn.commit()
    return one_result[0]


async def check_subject(conn, subject):
    subject.discipline_id = await test_entities(conn, "Discipline", subject.name)
    for i in subject.groups:
        group = await test_entities(conn, "group", i)
        await set_subject(conn, subject, group)


async def open_file(id, conn, err):
    with open(f"{html_save_path}{id}.html", "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        try:
            await timetable_analise(soup, conn)
        except Exception:
            print(f"Ошибка при обработке id={id}")
            err.append(id)


async def operate():
    conn = await aiosqlite.connect(db_path)
    cur = await conn.cursor()
    await cur.execute(clear_old_sql_request)
    await cur.execute(set_unchecked_mode_sql_request)

    errors = []
    for i in range(1, teachers_count):
        print("обработка расписания преподавателя " + str(i))
        await open_file(i, conn, errors)
    print(f"Ошибки в обработке:{errors}")
    asyncio.


if __name__ == '__main__':
    asyncio.run(operate())
