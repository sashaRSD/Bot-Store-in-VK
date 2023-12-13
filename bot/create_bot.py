from vkbottle.bot import Bot
from vkbottle import Keyboard, KeyboardButtonColor, Text
from dir_base import sqlite_db
import configparser

config = configparser.ConfigParser()
config.read("bot/config.ini")
bot = Bot(config["TOKEN"]["token_bot_vk"])
admin_id = int(config["TOKEN"]["admin_id"])


async def ret_keyboard(user_id):
    user = await sqlite_db.sql_read_id(user_id)
    if user[0][1]:
        keyboard_main = Keyboard().add(Text("Магазин", {"cmd": "store"}), color=KeyboardButtonColor.POSITIVE).row() \
            .add(Text(f"--> {user[0][1]}, {user[0][2]} <--", {"cmd": "reg"}), color=KeyboardButtonColor.POSITIVE).row() \
            .add(Text("Тестирование", {"cmd": "menu"}), color=KeyboardButtonColor.PRIMARY).row() \
            .add(Text("Обратная связь", {"cmd": "call"})) \
            .add(Text("Поддержать автора", {"cmd": "donat"}))
    else:
        keyboard_main = Keyboard().add(Text("Магазин", {"cmd": "store"}), color=KeyboardButtonColor.POSITIVE).row() \
            .add(Text("Зарегестрироваться", {"cmd": "reg"}), color=KeyboardButtonColor.NEGATIVE).row() \
            .add(Text("Тестирование", {"cmd": "menu"}), color=KeyboardButtonColor.PRIMARY).row() \
            .add(Text("Обратная связь", {"cmd": "call"})) \
            .add(Text("Поддержать автора", {"cmd": "donat"}))
    return keyboard_main
