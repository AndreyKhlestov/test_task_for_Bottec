from aiogram import types
from aiogram.dispatcher import FSMContext

from tg_bot.bot.utils import setup_django_settings  # установка Django настроек
from bot_Django.settings import MEDIA_ROOT
from tg_bot.bot.config import bot_logger, per_page_subcategories
from tg_bot.bot.loader import dp, bot
from tg_bot.bot.states.all_states import StateUser
from tg_bot.bot.keyboards.model_inline_keyboards import model_keyboards
from tg_bot.bot.keyboards.default_inline_keyboards import inline_keyboards
from tg_bot.bot.handlers.basket import view_shopping_cart
from tg_bot.models import Subcategory, Product


@dp.message_handler(text='Каталог', state='*')
async def category_menu(message: types.Message):
    """Запуск меню категорий"""
    bot_logger.debug(f"Пользователь {message.from_user.full_name} перешел в меню категорий")
    await StateUser.category_menu.set()
    await message.answer(text="Категории товаров:", reply_markup=model_keyboards())


@dp.callback_query_handler(lambda call: call.data.isdigit(), state=StateUser.category_menu)
async def choice_category(call: types.CallbackQuery):
    """Переход на другую страницу меню категорий"""
    bot_logger.debug(f"Пользователь {call.from_user.full_name} перешел на стр.{call.data} в меню категорий")
    await call.message.edit_text(text="Категории товаров:",
                                 reply_markup=model_keyboards(page_num=int(call.data)))


@dp.callback_query_handler(lambda call: not call.data.isdigit(), state=StateUser.category_menu)
async def start_subcategory_menu(call: types.CallbackQuery, state: FSMContext):
    """Запуск меню подкатегорий"""
    category = call.data
    bot_logger.debug(f"Пользователь {call.from_user.full_name} перешел в меню категории {category}")
    await StateUser.subcategory_menu.set()
    await state.update_data(selected_category=category)
    all_obj_model = Subcategory.objects.filter(category__name=category)
    if all_obj_model:
        await call.message.edit_text(text=f"Категория товаров - {category}", reply_markup=None)
        await call.message.answer(text=f"Подкатегория:",
                                  reply_markup=model_keyboards(all_obj_model, per_page_subcategories))
    else:
        await call.message.delete()


@dp.callback_query_handler(lambda call: call.data.isdigit(), state=StateUser.subcategory_menu)
async def choice_subcategory_menu(call: types.CallbackQuery, state: FSMContext):
    """Перемещение по страницам меню подкатегорий"""
    state_data = await state.get_data()
    category = state_data.get("selected_category")
    bot_logger.debug(f"Пользователь {call.from_user.full_name} перешел на стр.{call.data} "
                     f"в меню категории {category}")

    all_obj_model = Subcategory.objects.filter(category__name=category)
    await call.message.edit_text(text=call.message.text,
                                 reply_markup=model_keyboards(all_obj_model=all_obj_model,
                                                              per_page=per_page_subcategories,
                                                              page_num=int(call.data))
                                 )


@dp.callback_query_handler(lambda call: not call.data.isdigit(), state=StateUser.subcategory_menu)
async def send_products_subcategory_menu(call: types.CallbackQuery, state: FSMContext):
    """Выдача всех товаров выбранной подкатегории"""
    subcategory = call.data
    bot_logger.debug(f"Пользователь {call.from_user.full_name} перешел в подкатегорию {subcategory}.")
    await StateUser.choice_product.set()
    await call.message.edit_text(text=f"Подкатегория - {subcategory}", reply_markup=None)
    products = Product.objects.filter(subcategory__name=subcategory)
    for i_product in products:
        keyboards = inline_keyboards({i_product.id: "Добавить в корзину"})
        with open(f'{MEDIA_ROOT}/{i_product.image}', 'rb') as photo:
            await bot.send_photo(chat_id=call.from_user.id,
                                 photo=photo,
                                 caption=i_product.description,
                                 reply_markup=keyboards)


@dp.callback_query_handler(lambda call: call.data.isdigit(), state=StateUser.choice_product)
async def choice_product(call: types.CallbackQuery, state: FSMContext):
    """Уточнение количества товара"""
    id_product = call.data
    await state.update_data(id_selected_product=id_product)
    await call.message.answer(f"{Product.objects.get(id=id_product).name}\nУкажите количество товара")


@dp.message_handler(lambda message: message.text.isdigit(), state=StateUser.choice_product)
async def enter_quantity_product(message: types.Message, state: FSMContext):
    """Ввод количества товара для покупки"""
    quantity = int(message.text)
    if quantity > 0:
        state_data = await state.get_data()
        id_product = state_data.get("id_selected_product")
        await state.update_data(quantity_product=quantity)
        await message.answer(f"Подтвердите добавление в корзину следующего товара:\n"
                             f"{Product.objects.get(id=id_product).name} - {message.text}шт.",
                             reply_markup=inline_keyboards(["Подтвердить", "Отмена"]))
    else:
        await message.answer(f"Количество товара должно быть больше 0")


@dp.callback_query_handler(lambda call: not call.data.isdigit(), state=StateUser.choice_product)
async def confirmation_purchase(call: types.CallbackQuery, state: FSMContext):
    """Подтверждение введенного количества товара для добавления в корзину"""
    if call.data == "Отмена":
        await call.message.edit_text("Отмена покупки товара")
    elif call.data == "Подтвердить":
        from tg_bot.bot.utils.work_with_basket import add_to_cart
        state_data = await state.get_data()
        product_id = state_data.get("id_selected_product")
        quantity_product = state_data.get("quantity_product")
        add_to_cart(tg_user_id=call.from_user.id, product_id=product_id, quantity=int(quantity_product))
        await call.message.edit_text("Товар добавлен в корзину")
        await view_shopping_cart(call.from_user, state)
