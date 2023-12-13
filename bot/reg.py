from vkbottle import CtxStorage, BaseStateGroup
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message
from dir_base import sqlite_db
from bot import create_bot
bot = create_bot.bot
ctx = CtxStorage()


class RegData(BaseStateGroup):
    name = ""
    age = 0


@bot.on.private_message(text=["/reg <name> <age>"])
@bot.on.private_message(payload={"cmd": "reg"})
async def reg(message: Message, name=None, age=None):
    if not await sqlite_db.sql_read_id(message.from_id):
        await sqlite_db.sql_add_command(message.from_id)

    if name is not None and age is not None:
        await sqlite_db.sql_update(name.title(), age, message.from_id)
        await message.answer(f"Ваш ребенок - {name.title()}, его возвраст: {age}",
                             keyboard=await create_bot.ret_keyboard(message.from_id))
    else:
        await bot.state_dispenser.set(message.peer_id, RegData.name)
        keyboard_back = Keyboard().add(Text("Назад", {"cmd": "back_reg"}), color=KeyboardButtonColor.PRIMARY)
        user = await sqlite_db.sql_read_id(message.from_id)
        if user[0][1]:
            await message.answer(f"Вы можете изменить текущие данные - {user[0][1]}, {user[0][2]}\n"
                                 f"Для этого, введите имя вашего ребенка\n\n"
                                 f"Если передумали, то нажмите на кнопку <Назад>", keyboard=keyboard_back)
        else:
            await message.answer("Введите имя вашего ребенка", keyboard=keyboard_back)


@bot.on.message(state=RegData.name)
async def reg_name(message: Message):
    try:
        if eval(message.payload)['cmd'] == "back_reg":
            await back_reg(message)
            return 0
    except:
        ctx.set("name", message.text)
        await bot.state_dispenser.set(message.peer_id, RegData.age)
        return "Сколько лет вашему ребенку?"


@bot.on.message(state=RegData.age)
async def reg_age(message: Message):
    try:
        if eval(message.payload)['cmd'] == "back_reg":
            await back_reg(message)
            return 0
    except:
        try:
            age = int(message.text)
            if 3 < age < 99:
                await bot.state_dispenser.delete(message.peer_id)
                await sqlite_db.sql_update(ctx.get('name').title(), age, message.from_id)
                await message.answer(f"Ваш ребенок - {ctx.get('name').title()}, его возвраст: {age}",
                                     keyboard=await create_bot.ret_keyboard(message.from_id))
            else:
                await bot.state_dispenser.delete(message.peer_id)
                await sqlite_db.sql_update(ctx.get('name').title(), age, message.from_id)
                await message.answer("У нас нет игрушек для такого возвраста...\nНо следите за пополением каталога 😏",
                                     keyboard=await create_bot.ret_keyboard(message.from_id))
        except:
            await message.answer("Я вас не понимаю... O_o")


async def back_reg(message: Message):
    await bot.state_dispenser.delete(message.peer_id)
    await message.answer("Попробуйте позже 😉", keyboard=await create_bot.ret_keyboard(message.from_id))
