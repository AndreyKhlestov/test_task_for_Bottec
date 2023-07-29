from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

# from .config import BOT_TOKEN, bot_logger
from .config import BOT_TOKEN, bot_logger, redis_host, redis_port


bot_logger.info("Logger initialized")
bot = Bot(token=BOT_TOKEN)
storage = RedisStorage2(host=redis_host, port=redis_port)

# storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
