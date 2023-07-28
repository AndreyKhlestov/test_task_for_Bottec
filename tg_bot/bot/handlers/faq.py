import hashlib
from aiogram import types
from aiogram.dispatcher import FSMContext

from tg_bot.bot.utils import setup_django_settings  # установка Django настроек
from tg_bot.bot.loader import dp, bot
from tg_bot.bot.states.all_states import StateUser


faq_list = {
    "Что такое бот?": "Бот (от англ. robot) — программа, способная автоматически выполнять различные действия.",
    "Как связаться с администратором бота?": "Вы можете администратору бота в телеграмме @AndreyKhlestov.",
    "Почему нельзя оплатить заказ на сумму меньше 60 рублей?": "Это ограничения платежной системы YMoney",
    "Почему нельзя оплатить заказ на сумму больше 1000 рублей?":
        "Это ограничения платежной системы YMoney для тестовых платежей",
    "Как перезапустить бота?": "введите команду /start",
}


@dp.message_handler(text='FAQ', state='*')
async def start_faq(message: types.Message, state: FSMContext):
    """Запуск раздела FAQ"""
    await StateUser.faq.set()
    await message.answer("Вы в разделе FAQ.\n"
                         "Напишите ваш вопрос.")


@dp.inline_handler(state=StateUser.faq)
async def process_inline_query(query: types.InlineQuery):
    results = []
    for question, answer in faq_list.items():
        if query.query.lower() in question.lower():
            # Формируем ответ в формате InlineQueryResultArticle
            results.append(
                types.InlineQueryResultArticle(
                    id=hashlib.md5(question.encode()).hexdigest(),
                    title=question,
                    input_message_content=types.InputTextMessageContent(answer)
                )
            )
    await bot.answer_inline_query(query.id, results=results, cache_time=1)
