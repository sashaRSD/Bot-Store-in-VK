import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('dir_base/store_vk.db')
    cur = base.cursor()
    if base:
        print('Store database connect OK!')
    base.execute('CREATE TABLE IF NOT EXISTS data(name TEXT PRIMARY KEY, description TEXT, price INT, picture TEXT, '
                 'first_category BIT, second_category BIT, third_category BIT, fourth_category BIT)')
    base.commit()


async def sql_add_command(name, description, price, picture, first_category, second_category, third_category, fourth_category):
    cur.execute('INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (name, description, price, picture,
                                                            first_category, second_category, third_category, fourth_category))
    base.commit()


async def sql_read():
    return cur.execute('SELECT * FROM data').fetchall()


async def sql_read_name(data):
    return cur.execute('SELECT * FROM data WHERE name == ?', (data,)).fetchall()


async def sql_delete_command(data):
    start_changes = base.total_changes
    cur.execute('DELETE FROM data WHERE name == ?', (data,))
    base.commit()
    if (base.total_changes-start_changes) == 0:
        return 0
    return 1


async def sql_update(name, update, value):

    if update in ("1", "2", "3", "4"):
        if not (int(value) in (0, 1)):
            return 0

    if update in ('description', 'picture'):
        cur.execute('UPDATE data SET {} = ? WHERE name == ?'.format(update), (value, name))
    elif update in ('price', "1", "2", "3", "4"):
        cur.execute('UPDATE data SET {} = ? WHERE name == ?'.format(update), (int(value), name))
    else:
        print('No update...\n')
        return 0
    base.commit()
    return 1

