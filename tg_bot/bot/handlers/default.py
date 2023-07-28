from aiogram import types
from aiogram.dispatcher import FSMContext

from ..utils import setup_django_settings  # загрузка Django настроек
from ..config import bot_logger, link_group, link_channel
from ..loader import dp
from ..utils.check_subscription import checking_subscription
from ..keyboards.default_reply_keyboard import reply_keyboards

from tg_bot.models import Profile


async def main_menu(message: types.Message):
    """Переход в главное меню после старта"""
    text = "Добро пожаловать в телеграм магазин."
    button_main_menu = ["Каталог", "Корзина", "FAQ"]
    await message.answer(text=text, reply_markup=reply_keyboards(button_main_menu))


@dp.message_handler(commands="start", state=["*"])
async def info_subscription(message: types.Message, state: FSMContext):
    """Получение информации о подписках пользователя и при наличии таковых переход в главное меню"""
    bot_logger.info(f"Пользователь {message.from_user.full_name} ввел команду /start")
    add_text = "\n После подписки введите команду /start для повторной проверки."

    subscr_group = await checking_subscription(user_id=message.from_user.id, link=link_group)
    subscr_channel = await checking_subscription(user_id=message.from_user.id, link=link_channel)

    if subscr_group and subscr_channel:
        Profile.objects.get_or_create(
            tg_user_id=message.from_user.id,
            defaults={
                'name': message.from_user.username
            }
        )
        await state.reset_state()
        await main_menu(message)
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
    await message.answer("test")
    from tg_bot.models import TelegramMessage
    a, created = TelegramMessage.objects.get_or_create(text="fsdfasfsadfasfasdfasdfasfas")
    a.save()
