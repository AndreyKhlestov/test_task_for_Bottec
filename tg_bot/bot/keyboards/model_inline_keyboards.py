from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.db.models.query import QuerySet
from django.core.paginator import Paginator

from tg_bot.models import Category
from tg_bot.bot.config import per_page_categories


def model_keyboards(all_obj_model: QuerySet = Category.objects.all(),
                    per_page: int = per_page_categories,
                    page_num: int = 1, ) -> InlineKeyboardMarkup:
    """
    Inline клавиатура для элементов модели, у которых есть атрибут 'name' (категорий, подкатегорий, товаров).
    Получает список элементов модели, количество элементов на странице и номер отображаемой страницы.
    Возвращает inline клавиатуру из их имён.
    В конец кнопок добавляет кнопки навигации по страницам, если страниц больше 1.
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

    buttons_navigation = list()
    # Добавляем кнопки для навигации по страницам
    if page.has_previous():
        buttons_navigation.append(InlineKeyboardButton(text=" << ", callback_data=page.previous_page_number()))

    if page.has_next():
        buttons_navigation.append(InlineKeyboardButton(text=" >> ", callback_data=page.next_page_number()))
    keyboards.add(*buttons_navigation)

    return keyboards
