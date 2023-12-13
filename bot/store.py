from vkbottle import template_gen, TemplateElement
from vkbottle import Keyboard, VKPay
from vkbottle import GroupEventType, GroupTypes
from vkbottle.bot import Message
from dir_base import sqlite_store, sqlite_db
from bot import create_bot
import random
bot = create_bot.bot


@bot.on.private_message(text=['магазин', 'store'])
@bot.on.private_message(payload={"cmd": "store"})
async def store(message: Message):
    bd_read = await sqlite_store.sql_read()
    catalog_total = len(bd_read)
    catalog = ""
    for item in bd_read:
        catalog += await create_catalog(item[0], item[1], item[2], item[3], catalog_total, bd_read.index(item)+1)

    if (await sqlite_db.sql_read_id(message.from_id))[0][2]:
        await message.answer("Каталог:", template=catalog)
        await message.answer("Рекомендуем для Вас:", template=await person_catalog(message.from_id, bd_read))
    else:
        await message.answer("Каталог:", template=catalog)
    await message.answer("Магазин создан для обучающих целей!\n"
                         "НЕ нужно ничего покупать!!!")
    await message.answer(sticker_id=79395)


async def create_catalog(name, disc, price, picture, category_total, category_num):
    pay = (Keyboard(one_time=False, inline=True)
           .add(VKPay(payload={"name": name}, hash=f'action=pay-to-group&amount={price}&group_id={200932657}&aid=10')))
    if category_total == 1:
        element_catalog = template_gen(TemplateElement(name, f"Описание: {disc} \nСтоимость: {price} руб.",
                                                       f"{picture}", pay.get_json()))
    else:
        if category_num == 1:
            element_catalog = template_gen(TemplateElement(name, f"Описание: {disc} \nСтоимость: {price} руб.",
                                                           f"{picture}", pay.get_json()))[:-2]
        elif category_num == category_total:
            element_catalog = ", " + template_gen(
                TemplateElement(name, f"Описание: {disc} \nСтоимость: {price} руб.",
                                f"{picture}", pay.get_json()))[34:]
        else:
            element_catalog = ", " + template_gen(
                TemplateElement(name, f"Описание: {disc} \nСтоимость: {price} руб.",
                                f"{picture}", pay.get_json()))[34:-2]
    return element_catalog


async def person_catalog(user_id, bd_read):
    age = (await sqlite_db.sql_read_id(user_id))[0][2]
    category_index = 0
    if 3 <= age < 12:
        category_index = 4
    elif 12 <= age < 21:
        category_index = 5
    elif 21 <= age < 40:
        category_index = 6
    elif age >= 40:
        category_index = 7

    category_total = 0
    for item in bd_read:
        if item[category_index] == 1:
            category_total += 1

    category_num = 0
    personal_catalog = ""
    for item in bd_read:
        if item[category_index] == 1:
            category_num += 1
            personal_catalog += await create_catalog(item[0], item[1], item[2], item[3], category_total, category_num)
    return personal_catalog


@bot.on.raw_event(GroupEventType.VKPAY_TRANSACTION, dataclass=GroupTypes.VkpayTransaction)
async def vk_pay(event: GroupTypes.MessageEvent):
    await bot.api.messages.send(peer_id=event.object.user_id,
                                message="Оплата прошла успешно!\n"
                                        "В ближайшее время, с вами свяжутся для уточнения заказа.",
                                random_id=random.randint(1, 1000))
    await bot.api.messages.send(user_id=create_bot.admin_id,
                                message=f"Новый заказ от {event.object.user_id}\n"
                                        f"Покупака - {event.object.payload['name']}",
                                random_id=random.randint(1, 1000))

