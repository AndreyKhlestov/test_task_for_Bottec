from aiogram import types
from aiogram.dispatcher import FSMContext

from tg_bot.bot.utils import setup_django_settings  # установка Django настроек
from bot_Django.settings import MEDIA_ROOT
from tg_bot.bot.config import bot_logger, per_page_subcategories
from tg_bot.bot.loader import dp, bot
from tg_bot.bot.states.all_states import StateUser
from tg_bot.bot.keyboards.catalog_inline_keyboards import catalog_keyboards
from tg_bot.bot.keyboards.default_inline_keyboards import inline_keyboards
from tg_bot.models import Profile


@dp.message_handler(text='Корзина', state='*')
async def start_shopping_cart(message: types.Message, state: FSMContext):
    """Запуск меню корзины"""
    await view_shopping_cart(from_user=message.from_user, state=state)


async def view_shopping_cart(from_user: types.User, state: FSMContext):
    """Просмотр корзины"""
    bot_logger.debug(f"Пользователь {from_user.full_name} перешел в меню корзины")
    await StateUser.view_shopping_cart.set()
    user = Profile.objects.get(tg_user_id=from_user.id)
    basket = user.basket()
    # keyword = inline_keyboards([])
    await bot.send_message(chat_id=from_user.id, text=basket)
