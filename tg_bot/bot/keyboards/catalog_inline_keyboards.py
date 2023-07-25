from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.db.models.query import QuerySet
from django.core.paginator import Paginator

from tg_bot.models import Category, Subcategory
from tg_bot.bot.config import per_page_categories


def catalog_keyboards(all_obj_model: QuerySet = Category.objects.all(),
                      per_page: int = per_page_categories,
                      page_num: int = 1,) -> None or InlineKeyboardMarkup:
    """
    Inline клавиатура для элементов 'Каталога' (категорий и подкатегорий).
    Получает список элементов категорий/подкатегорий, количество элементов на странице и номер отображаемой страницы.
    Возвращает inline клавиатуру из их имён.
    В конец кнопок добавляет две кнопки навигации по страницам, если страниц больше 1
    """
    all_obj_model = list(all_obj_model)
    # Разбиваем на страницы с пагинацией
    model_paginator = Paginator(object_list=all_obj_model, per_page=per_page, allow_empty_first_page=True)

    # Т.к. Paginator автоматически обработает все ошибки, связанные с номером страницы,
    # то правильный номер страницы получим из самой страницы, которую выдаст Paginator
    page = model_paginator.get_page(page_num)
    # return catalog_keyboards(model_paginator.get_page(page.number))

    keyboards = InlineKeyboardMarkup(row_width=2)
    for i_object in model_paginator.get_page(page.number):
        keyboards.add(InlineKeyboardButton(text=i_object.name, callback_data=i_object.name))
    if not page.has_other_pages():
        return keyboards

    # Добавляем кнопки для навигации по страницам
    if page.has_previous():
        data_button_back = page.previous_page_number()
        text_button_back = " << "
    else:
        # data_button_back = page.number
        data_button_back = 0
        text_button_back = "    "
    if page.has_next():
        data_button_next = page.next_page_number()
        text_button_next = " >> "
    else:
        # data_button_next = page.number
        data_button_next = 0
        text_button_next = "    "
    keyboards.add(*[
        InlineKeyboardButton(text=text_button_back, callback_data=data_button_back),
        InlineKeyboardButton(text=text_button_next, callback_data=data_button_next),
    ])

    return keyboards
