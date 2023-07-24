from loader import bot


async def checking_subscription(user_id: int, link: str):
    user_channel_status = await bot.get_chat_member(
        chat_id=link,
        user_id=user_id
    )
    if user_channel_status["status"] != "left":
        return True
    else:
        return False
