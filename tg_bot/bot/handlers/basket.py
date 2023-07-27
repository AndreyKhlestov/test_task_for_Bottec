from aiogram import types
from aiogram.dispatcher import FSMContext

from tg_bot.bot.utils import setup_django_settings  # установка Django настроек
from tg_bot.bot.utils.work_with_basket import del_product
from tg_bot.bot.config import bot_logger
from tg_bot.bot.loader import dp, bot
from tg_bot.bot.states.all_states import StateUser
from tg_bot.bot.keyboards.delete_products_keyboard import del_product_keyboards
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
    if basket.order_items.count() == 0:
        await bot.send_message(chat_id=from_user.id, text="Корзина пуста")
    else:
        keyboard = inline_keyboards(["Удалить товар", "Оформить покупку"])
        await bot.send_message(chat_id=from_user.id, text=basket, reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == "Удалить товар", state=StateUser.view_shopping_cart)
@dp.callback_query_handler(lambda call: not call.data.isdigit(), state=StateUser.delete_products)
async def menu_delete_products(call: types.CallbackQuery, state: FSMContext):
    """Запуск меню удаления товаров из корзины"""
    await call.message.delete()
    if call.data == "Назад":
        await view_shopping_cart(call.from_user, state)

    elif call.data == "Удалить товар":
        await StateUser.delete_products.set()
        basket = Profile.objects.get(tg_user_id=call.from_user.id).basket()
        keyboard = del_product_keyboards(all_obj_model=basket.order_items.all())
        await call.message.answer(text="Выберете товар для удаления:", reply_markup=keyboard)

    else:
        basket = del_product(tg_user_id=call.from_user.id, product_name=call.data)
        await call.message.answer(text=f"Товар '{call.data}' удален из корзины",)
        if basket.order_items.count() == 0:
            await view_shopping_cart(call.from_user, state)
        else:
            keyboard = del_product_keyboards(all_obj_model=basket.order_items.all())
            await call.message.answer(text="Выберете товар для удаления:", reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data.isdigit(), state=StateUser.delete_products)
async def menu_delete_products(call: types.CallbackQuery, state: FSMContext):
    basket = Profile.objects.get(tg_user_id=call.from_user.id).basket()
    await call.message.edit_reply_markup(
        del_product_keyboards(all_obj_model=basket.order_items.all(), page_num=call.data)
    )

