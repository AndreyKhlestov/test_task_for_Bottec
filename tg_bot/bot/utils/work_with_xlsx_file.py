import openpyxl
import os
import aiofiles

from ..config import xlsx_file_name
from tg_bot.models import Order


def create_or_load_excel_file():
    if not os.path.exists(xlsx_file_name):
        # Если файл не существует, создаем новый с заголовками
        headers = ["Id заказа", "Имя пользователя", "ID Telegram пользователя", "Сумма", "Дата"]
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(headers)
    else:
        # Если файл существует, загружаем его и получаем активный лист
        workbook = openpyxl.load_workbook(xlsx_file_name)
        sheet = workbook.active

    return workbook, sheet


async def append_new_payments(order: Order):
    workbook, sheet = create_or_load_excel_file()
    # Дозаписываем новые данные
    sheet.append([order.id,
                  order.profile.name,
                  order.profile.tg_user_id,
                  order.total_cost,
                  order.payment_datetime.replace(tzinfo=None)])

    # Сохраняем изменения в файле
    async with aiofiles.open(xlsx_file_name, 'wb') as f:
        workbook.save(xlsx_file_name)
