from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.db.models.query import QuerySet

from tg_bot.bot.config import per_page_categories
from .model_inline_keyboards import model_keyboards
from tg_bot.models import Product
from ..config import per_page_delete_product


def del_product_keyboards(all_obj_model: QuerySet,
                          per_page: int = per_page_delete_product,
                          page_num: int = 1) -> InlineKeyboardMarkup:
    """Inline клавиатура для меню удаления товаров из корзины."""
    products = Product.objects.filter(order_items__in=all_obj_model)
    keyboards = model_keyboards(products, per_page, page_num)
    keyboards.add(InlineKeyboardButton(text="Назад", callback_data="Назад"))
    return keyboards
