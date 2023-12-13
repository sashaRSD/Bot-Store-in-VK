from vkbottle.bot import Message
from dir_base import sqlite_store
from bot import create_bot
bot = create_bot.bot

@bot.on.private_message(func=lambda message: message.text.startswith('/new') and message.from_id == create_bot.admin_id)
async def add_item(message: Message):
    try:
        text = message.text.split("\n")
        text.pop(0)
        for i in range(len(text)):
            if text[i][-1] == ' ':
                text[i] = text[i].rstrip()
        await sqlite_store.sql_add_command(text[0], text[1], int(text[2]), text[3],
                                           int(text[4][0]), int(text[4][1]), int(text[4][2]), int(text[4][3]))
        await message.answer(f"Товар {text[0]} успешно добавлен!")
    except:
        await message.answer("Ошибка добавления товара, что то пошло не так...\n\n"
                             "Пример:\n"
                             "/new\n"
                             "Алеша Попович\n"
                             "Крутая игрушка\n"
                             "12\n"
                             "-200932657_457239099\n"
                             "1000")


@bot.on.private_message(func=lambda message: message.text.startswith('/del') and message.from_id == create_bot.admin_id)
async def del_item(message: Message):
    try:
        text = message.text.split("/del ")
        if not await sqlite_store.sql_delete_command(text[1]):
            raise NameError('No delete...')
        await message.answer(f"Товар {text[1]} успешно удален!")
    except:
        text = ""
        bd_read = await sqlite_store.sql_read()
        for item in bd_read:
            text += f"{item[0]}\n"
        await message.answer(f"Ошибка удаления товара, что то пошло не так...\n\n"
                             f"Доступные имена:\n"
                             f"{text}")


@bot.on.private_message(func=lambda message: message.text.startswith('/upd') and message.from_id == create_bot.admin_id)
async def upd_item(message: Message):
    try:
        text = message.text.split("\n")
        text.pop(0)
        for i in range(len(text)):
            if text[i][-1] == ' ':
                text[i] = text[i].rstrip()
        if not await sqlite_store.sql_update(text[0], text[1], text[2]):
            raise NameError('No update...')
        await message.answer(f"Товар {text[0]} успешно изменен! \n Теперь {text[1]}={text[2]}")
    except:
        text = ""
        bd_read = await sqlite_store.sql_read()
        for item in bd_read:
            text += f"\t{item[0]}\n"
        await message.answer(f"Ошибка изменения товара, что то пошло не так...\n\n"
                             f"Пример:\n"
                             f"/upd\n"
                             f"Алеша Попович\n"
                             f"Option name\n"
                             f"New value\n\n"
                             f"Доступные имена:\n"
                             f"{text}\n\n"
                             f"Доступные поля:\n"
                             f"description - описание\n"
                             f"price - цена\n"
                             f"picture - картинка\n"
                             f"1 - категория 3-12 лет\n"
                             f"2 - категория 12-21 год\n"
                             f"3 - категория 21-40 лет\n"
                             f"4 - категория 40+лет\n")


@bot.on.private_message(func=lambda message: message.text.startswith('/info') and message.from_id == create_bot.admin_id)
async def info_item(message: Message):
    try:
        text = message.text.split("/info ")
        print(text)
        item_info = await sqlite_store.sql_read_name(text[1])
        print(item_info)
        if not item_info:
            raise NameError('No info...')
        await message.answer(f"Товар {item_info[0][0]}\n"
                             f"Описание: {item_info[0][1]}\n"
                             f"Цена: {item_info[0][2]}\n"
                             f"Фото: {item_info[0][3]}\n"
                             f"Категория 3-12 лет: {item_info[0][4]}\n"
                             f"Категория 12-21 год: {item_info[0][5]}\n"
                             f"Категория 21-40 лет: {item_info[0][6]}\n"
                             f"Категория 40+лет: {item_info[0][7]}")
    except:
        text = ""
        bd_read = await sqlite_store.sql_read()
        for item in bd_read:
            text += f"{item[0]}\n"
        await message.answer(f"Доступные имена:\n"
                             f"{text}")
