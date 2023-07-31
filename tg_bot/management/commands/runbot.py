from django.core.management.base import BaseCommand
from aiogram import executor

from tg_bot.bot.config import bot_logger
from tg_bot.bot.loader import dp
from tg_bot.bot import handlers


class Command(BaseCommand):
    """Кастомная команда Джанго, для запуска телеграм бота."""
    help = 'Starting a telegram bot'

    def handle(self, *args, **options):
        bot_logger.info('Запуск бота')

        #####################
        import asyncio
        from tg_bot.bot.utils.send_message_all_users import send_message_to_all_users
        loop = asyncio.get_event_loop()
        loop.create_task(send_message_to_all_users())
        #####################

        executor.start_polling(dp, skip_updates=True)
