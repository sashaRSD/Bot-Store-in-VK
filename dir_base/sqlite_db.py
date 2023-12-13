import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('dir_base/base_vk.db')
    cur = base.cursor()
    if base:
        print('Data base connect OK!')
    base.execute('CREATE TABLE IF NOT EXISTS data(id INT PRIMARY KEY, name TEXT, age INT)')
    base.commit()


async def sql_add_command(id):
    cur.execute('INSERT INTO data VALUES (?, ?, ?)', (id, None, None))
    base.commit()


async def sql_read_id(data):
    return cur.execute('SELECT * FROM data WHERE id == ?', (data,)).fetchall()


async def sql_update(name, age, id):
    cur.execute('UPDATE  data SET name = ?, age = ? WHERE id == ?', (name, age, id))
    base.commit()

