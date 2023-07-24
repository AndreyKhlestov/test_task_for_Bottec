import os
from dotenv import load_dotenv, find_dotenv

from logs.logs_setup import loggers


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


"""Tokens"""
BOT_TOKEN = os.getenv("BOT_TOKEN")

"""Loggers"""
bot_logger = loggers['BotLogger']

"""Redis"""
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")


"""Links"""
link_group = os.getenv("LINK_GROUP")
link_channel = os.getenv("LINK_CHANNEL")
