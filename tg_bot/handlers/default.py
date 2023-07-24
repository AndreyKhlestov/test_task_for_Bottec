from aiogram import types

from config import bot_logger, link_group, link_channel
from loader import dp
from utils.check_subscription import checking_subscription


@dp.message_handler(commands="start", state=["*"])
async def info_subscription(message: types.Message):
    bot_logger.info(
        f"Пользователь {message.from_user.full_name} ввел команду /start"
    )
    add_text = ("\nПосле подписки введите команду /start "
                "для повторной проверки.")
    subscr_group = await checking_subscription(user_id=message.from_user.id,
                                               link=link_group)
    subscr_channel = await checking_subscription(user_id=message.from_user.id,
                                                 link=link_channel)
    if subscr_group and subscr_channel:
        await message.answer("Подписан")
    elif not (subscr_group or subscr_channel):
        await message.answer(
            f"Подпишитесь на канал {link_channel} и группу {link_group}."
            f"{add_text}"
        )
    elif not subscr_group:
        await message.answer(f"Подпишитесь на группу {link_group}."
                             f"{add_text}")
    else:
        await message.answer(f"Подпишитесь на канал {link_channel}."
                             f"{add_text}")


@dp.message_handler(commands="help", state=["*"])
async def help(message: types.Message):
    await message.answer("Для запуска или перезапуска бота напишите /start")


@dp.message_handler(commands="test", state=["*"])
async def test(message: types.Message):
    dp.message_handlers.clear()
    dp.callback_query_handlers.clear()
    dp.inline_query_handlers.clear()
    dp.chosen_inline_result_handlers.clear()
    dp.poll_answer_handlers.clear()
    await message.answer("Тест")
