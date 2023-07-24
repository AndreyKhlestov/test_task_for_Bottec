from aiogram import executor
from config import bot_logger
from loader import dp
from handlers import default


if __name__ == '__main__':
    bot_logger.info('Запуск бота')
    executor.start_polling(dp, skip_updates=True)
