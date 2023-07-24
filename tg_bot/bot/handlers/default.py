# import os
# import django
from aiogram import types

# # Устанавливаем переменные окружения DJANGO_SETTINGS_MODULE для указания пути до settings.py Django проекта
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_Django.bot_Django.settings')
# os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
# django.setup()
from ..utils import setup_django_settings
from ..config import bot_logger, link_group, link_channel
from ..loader import dp
from ..utils.check_subscription import checking_subscription
from tg_bot.models import Profile


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_Django.bot_Django.settings')
# os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
# django.setup()


# from config import bot_logger, link_group, link_channel
# from loader import dp
# from utils.check_subscription import checking_subscription


@dp.message_handler(commands="start", state=["*"])
async def info_subscription(message: types.Message):
    """Получение информации о подписках пользователя и при наличии таковых переход в главное меню"""
    bot_logger.info(f"Пользователь {message.from_user.full_name} ввел команду /start")
    add_text = "\n После подписки введите команду /start для повторной проверки."

    subscr_group = await checking_subscription(user_id=message.from_user.id, link=link_group)
    subscr_channel = await checking_subscription(user_id=message.from_user.id, link=link_channel)

    if subscr_group and subscr_channel:
        user, created = Profile.objects.get_or_create(
            tg_user_id=message.from_user.id,
            defaults={
                'name': message.from_user.username
            }
        )
        await message.answer("Подписан")
    elif not (subscr_group or subscr_channel):
        await message.answer(f"Подпишитесь на канал {link_channel} и группу {link_group}.{add_text}")
    elif not subscr_group:
        await message.answer(f"Подпишитесь на группу {link_group}.{add_text}")
    else:
        await message.answer(f"Подпишитесь на канал {link_channel}.{add_text}")


@dp.message_handler(commands="help", state=["*"])
async def help(message: types.Message):
    await message.answer("Для запуска или перезапуска бота напишите /start")


@dp.message_handler(commands="test", state=["*"])
async def test(message: types.Message):
    await message.answer("Тест")
