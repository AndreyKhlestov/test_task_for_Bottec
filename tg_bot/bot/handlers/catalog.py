from aiogram import types
from aiogram.dispatcher import FSMContext

from tg_bot.bot.utils import setup_django_settings  # загрузка Django настроек
from tg_bot.bot.config import bot_logger, per_page_subcategories
from tg_bot.bot.loader import dp
from tg_bot.bot.states.all_states import StateUser
from tg_bot.bot.keyboards.catalog_inline_keyboards import catalog_keyboards
from tg_bot.models import Subcategory


@dp.message_handler(text='Каталог', state='*')
async def category_menu(message: types.Message):
    """Запуск меню категорий"""
    bot_logger.debug(f"Пользователь {message.from_user.full_name} перешел в меню категорий")
    await StateUser.category_menu.set()
    await message.answer(text="Категории товаров:", reply_markup=catalog_keyboards())


@dp.callback_query_handler(lambda call: call.data.isdigit(), state=StateUser.category_menu)
async def choice_category(call: types.CallbackQuery):
    """Переход на другую страницу меню категорий"""
    if call.data != "0":
        bot_logger.debug(f"Пользователь {call.message.from_user.full_name} перешел на стр.{call.data} в меню категорий")
        await call.message.edit_text(text="Категории товаров:",
                                     reply_markup=catalog_keyboards(page_num=int(call.data)))


@dp.callback_query_handler(lambda call: not call.data.isdigit(), state=StateUser.category_menu)
async def start_subcategory_menu(call: types.CallbackQuery, state: FSMContext):
    """Запуск меню подкатегорий"""
    category = call.data
    bot_logger.debug(f"Пользователь {call.message.from_user.full_name} перешел в меню подкатегорий {category}")
    await StateUser.subcategory_menu.set()
    await state.update_data(selected_category=category)
    all_obj_model = Subcategory.objects.filter(category__name=category)
    if all_obj_model:
        await call.message.edit_text(text=f"Категория - {category}",
                                     reply_markup=catalog_keyboards(all_obj_model, per_page_subcategories))
    else:
        await call.message.delete()


@dp.callback_query_handler(lambda call: call.data.isdigit(), state=StateUser.subcategory_menu)
async def start_subcategory_menu(call: types.CallbackQuery, state: FSMContext):
    if call.data != "0":
        state_data = await state.get_data()
        category = state_data.get("selected_category")
        bot_logger.debug(f"Пользователь {call.message.from_user.full_name} перешел на стр.{call.data} "
                         f"в меню подкатегорий {category}")

        all_obj_model = Subcategory.objects.filter(category__name=category)
        await call.message.edit_text(text=call.message.text,
                                     reply_markup=catalog_keyboards(all_obj_model=all_obj_model,
                                                                    per_page=per_page_subcategories,
                                                                    page_num=int(call.data))
                                     )


@dp.callback_query_handler(lambda call: not call.data.isdigit(), state=StateUser.subcategory_menu)
async def start_subcategory_menu(call: types.CallbackQuery, state: FSMContext):
    await StateUser.choice_product.set()
