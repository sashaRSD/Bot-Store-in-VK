from vkbottle import GroupEventType, GroupTypes, VKAPIError
from bot import create_bot
import random
bot = create_bot.bot

@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    try:
        await bot.api.messages.send(peer_id=event.object.user_id,
                                    message="Добро пожаловать во вселенную Трех Богатырей!",
                                    random_id=random.randint(1, 1000))
    except VKAPIError:
        pass


@bot.on.raw_event(GroupEventType.GROUP_LEAVE, dataclass=GroupTypes.GroupLeave)
async def group_leave_handler(event: GroupTypes.GroupLeave):
    try:
        await bot.api.messages.send(peer_id=event.object.user_id,
                                    message="До новых встреч!",
                                    random_id=random.randint(1, 1000))
    except VKAPIError:
        pass