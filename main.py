from vkbottle import Keyboard, Text, OpenLink
from vkbottle.bot import Message
from dir_base import sqlite_db, sqlite_store
from bot import create_bot, event, reg, store, test, base_message
import asyncio
import logging

bot = create_bot.bot
logging.getLogger("vkbottle").setLevel(logging.INFO)


@bot.on.private_message(text=['Начать', 'start', 'старт'])
async def start(message: Message):
    if not await sqlite_db.sql_read_id(message.from_id):
        await sqlite_db.sql_add_command(message.from_id)
    user = (await bot.api.users.get(message.from_id))[0]
    await message.answer(f"Привет, {user.first_name}", keyboard=await create_bot.ret_keyboard(message.from_id))
    await message.answer("⬇⬇⬇", keyboard=Keyboard(inline=True).add(Text("Зарегестрироваться", {"cmd": "reg"})))


@bot.on.private_message(payload={"cmd": "donat"})
async def donat(message: Message):
    keyboard = Keyboard(inline=True).add(OpenLink('https://www.tinkoff.ru/cf/71ARxuIBdob', 'Жми сюда!'))
    await message.answer("Поддержать автора копейкой ;)", keyboard=keyboard)


@bot.on.private_message(payload={"cmd": "call"})
async def call(message: Message):
    await message.answer('Наши контактные данные: \n'
                         'Электронная почта - kaa.1999@mail.ru \n'
                         'Username ВК - @sasha_rsd')


@bot.on.private_message(sticker=73601)
async def sticker(message: Message):
    await message.answer(sticker_id=75)


@bot.on.private_message(func=lambda message: message.from_id == create_bot.admin_id, attachment="sticker")
async def sticker_id(message: Message):
    await message.answer(f"Sticker ID: {message.attachments[0].sticker.sticker_id}")


@bot.on.private_message()
async def menu(message: Message):
    if not await sqlite_db.sql_read_id(message.from_id):
        await sqlite_db.sql_add_command(message.from_id)
    await message.answer("Меня такому еще не научили...\n"
                         "Попробуйте выбрать вариант на клавиатуре", keyboard=await create_bot.ret_keyboard(message.from_id))
    await message.answer(sticker_id=77713)


if __name__ == '__main__':
    sqlite_db.sql_start()
    sqlite_store.sql_start()
    asyncio.run(bot.run_polling())



