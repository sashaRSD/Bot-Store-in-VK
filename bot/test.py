from vkbottle import PhotoMessageUploader
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink
from vkbottle import GroupEventType, GroupTypes, Callback
from vkbottle.bot import Message
import random
from bot import create_bot
bot = create_bot.bot


@bot.on.private_message(payload={"cmd": "menu"})
async def menu(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text("🗿", {"cmd": "test"}), color=KeyboardButtonColor.PRIMARY).row()
    keyboard.add(OpenLink("https://www.youtube.com/watch?v=8vPQKM5UOJU", "Подсказка")).row()
    keyboard.add(Text("Назад", {"cmd": "back_test"}), color=KeyboardButtonColor.POSITIVE)
    await message.answer("У нас тут серьезные вопросы!", keyboard=keyboard)


@bot.on.private_message(payload={"cmd": "test"})
async def test(message: Message):
    stone = await PhotoMessageUploader(bot.api).upload('foto/stone.jpg')
    stone_message = await message.answer(attachment=stone)
    keyboard_message = await message.answer("Нужно сделать выбор 🙄")
    keyboard = (
            Keyboard(inline=True)
            .add(Callback("←", {"del_stone": stone_message.message_id,
                                "del_message": keyboard_message.message_id,
                                'com': '←'}), color=KeyboardButtonColor.POSITIVE)
            .add(Callback("↑", {"del_stone": stone_message.message_id,
                                "del_message": keyboard_message.message_id,
                                'com': '↑'}), color=KeyboardButtonColor.NEGATIVE)
            .add(Callback("→", {"del_stone": stone_message.message_id,
                                "del_message": keyboard_message.message_id,
                                'com': '→'}), color=KeyboardButtonColor.PRIMARY)
    )
    await bot.api.messages.edit(peer_id=keyboard_message.peer_id, message_id=keyboard_message.message_id,
                                message="Нужно сделать выбор 🙄", keyboard=keyboard.get_json())


@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def end(event: GroupTypes.MessageEvent):

    await bot.api.messages.send_message_event_answer(event_id=event.object.event_id,
                                                     peer_id=event.object.peer_id,
                                                     user_id=event.object.user_id)
    if event.object.payload['com'] == '←':
        await bot.api.messages.delete(peer_id=event.object.peer_id, message_ids=event.object.payload['del_stone'], delete_for_all=True)
        await bot.api.messages.delete(peer_id=event.object.peer_id, message_ids=event.object.payload['del_message'], delete_for_all=True)
        await bot.api.messages.send(peer_id=event.object.user_id,
                                    message="Богатым будешь!",
                                    random_id=random.randint(1, 1000),
                                    keyboard=await create_bot.ret_keyboard(event.object.user_id))
    elif event.object.payload['com'] == '↑':
        await bot.api.messages.delete(peer_id=event.object.peer_id, message_ids=event.object.payload['del_stone'], delete_for_all=True)
        await bot.api.messages.delete(peer_id=event.object.peer_id, message_ids=event.object.payload['del_message'], delete_for_all=True)
        tugar = await PhotoMessageUploader(bot.api).upload('foto/zlo.jpg')
        await bot.api.messages.send(peer_id=event.object.user_id,
                                    attachment=tugar,
                                    random_id=random.randint(1, 1000),
                                    keyboard=await create_bot.ret_keyboard(event.object.user_id))
    elif event.object.payload['com'] == '→':
        await bot.api.messages.delete(peer_id=event.object.peer_id, message_ids=event.object.payload['del_stone'], delete_for_all=True)
        await bot.api.messages.delete(peer_id=event.object.peer_id, message_ids=event.object.payload['del_message'], delete_for_all=True)
        await bot.api.messages.send(peer_id=event.object.user_id,
                                    message="Женатым будешь!",
                                    random_id=random.randint(1, 1000),
                                    keyboard=await create_bot.ret_keyboard(event.object.user_id))


@bot.on.private_message(payload={"cmd": "back_test"})
async def back(message: Message):
    await message.answer("Попробуйте позже 😉", keyboard=await create_bot.ret_keyboard(message.from_id))
