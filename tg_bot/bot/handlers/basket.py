from aiogram import types
from aiogram.dispatcher import FSMContext

from tg_bot.bot.utils import setup_django_settings  # установка Django настроек
from tg_bot.bot.utils.work_with_basket import del_product
from tg_bot.bot.config import bot_logger, provider_token
from tg_bot.bot.loader import dp, bot
from tg_bot.bot.states.all_states import StateUser
from tg_bot.bot.keyboards.delete_products_keyboard import del_product_keyboards
from tg_bot.bot.keyboards.default_inline_keyboards import inline_keyboards
from tg_bot.bot.keyboards.yes_or_no_inline_keyboards import yes_or_no_keyboards
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
        # text = f"Корзина:\n\n{basket}\n\nОбщая сумма:     {basket.total_cost} руб."
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


@dp.callback_query_handler(lambda call: call.data == "Нет", state=StateUser.confirmation_address)
@dp.callback_query_handler(lambda call: call.data == "Оформить покупку", state=StateUser.view_shopping_cart)
async def start_enter_address(call: types.CallbackQuery, state: FSMContext):
    """Начало процедуры ввода адреса"""
    basket = Profile.objects.get(tg_user_id=call.from_user.id).basket()
    if basket.total_cost < 60:
        await call.answer("Заказ должен быть не меньше 60 руб.", show_alert=True)
    else:
        await call.message.delete()
        address = basket.address

        if call.data == "Нет":
            address = None

        if address:
            await call.message.answer(f"Адрес доставки:\n{address}", reply_markup=yes_or_no_keyboards())
            await StateUser.confirmation_address.set()
        else:
            await StateUser.enter_address.set()
            await call.message.answer("Введите адрес доставки")


@dp.message_handler(state=StateUser.enter_address)
async def enter_address(message: types.Message, state: FSMContext):
    """Подтверждение адреса доставки"""
    await StateUser.confirmation_address.set()
    basket = Profile.objects.get(tg_user_id=message.from_user.id).basket()
    basket.address = message.text
    basket.save()
    await message.answer(f"Адрес доставки:\n{message.text}", reply_markup=yes_or_no_keyboards())


@dp.callback_query_handler(lambda call: call.data == "Да", state=StateUser.confirmation_address)
async def confirmation_address(call: types.CallbackQuery, state: FSMContext):
    """Отправка кнопки оплаты"""
    await call.message.delete()
    basket = Profile.objects.get(tg_user_id=call.from_user.id).basket()
    prices = list()

    for item_order in basket.order_items.all():
        prices.append(types.LabeledPrice(
            label=f"{item_order.product.name} x {item_order.quantity}",
            amount=int(item_order.total_cost * 100)
        ))
    await bot.send_invoice(chat_id=call.from_user.id,
                           title=f"заказ № {basket.id}",  # наименование оплаты
                           description=" ",  # описание
                           payload=f"order_payment_{basket.id}",  # внутрення информация
                           provider_token=provider_token,  # токен платежной системы
                           currency="RUB",  # валюта
                           prices=prices,
                           start_parameter="start"
                           )


@dp.pre_checkout_query_handler(state="*")
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT, state="*")
async def process_pay(message: types.Message):
    order = Profile.objects.get(tg_user_id=message.from_user.id).basket()
    payment_total_cost = message.successful_payment.total_amount
    if payment_total_cost == order.total_cost*100:
        order.payment_status = True
        order.save()
    else:
        text = f"Сумма заказа не сходится с оплаченной суммой (вместо {order.total_cost} оплачено " \
               f" {payment_total_cost/100} руб.)\n"
        bot_logger.error_pay(f"Вероятность махинации при оплате.\n"
                             f"{text}"
                             f"Пользователь {message.from_user.full_name} - id {message.from_user.id}")

        await message.answer(f"Выявлена махинация при платеже.\n{text}"
                             f"Товар считается не оплаченным до выяснения всех обстоятельств.\n\n"
                             f"Обратитесь администратору бота")

