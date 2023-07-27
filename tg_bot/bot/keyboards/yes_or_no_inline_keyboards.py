from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_or_no_keyboards() -> InlineKeyboardMarkup:
    """Inline клавиатура для кнопок Да и Нет."""
    keyboards = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text="Да", callback_data="Да")
    no = InlineKeyboardButton(text="Нет", callback_data="Нет")
    keyboards.add(yes, no)
    return keyboards
