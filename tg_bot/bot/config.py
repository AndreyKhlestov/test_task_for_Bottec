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

"""Settings Paginator"""
per_page_categories = 5
per_page_subcategories = 4
per_page_delete_product = 6

"""Settings UKassa"""
provider_token = os.getenv("PROVIDER_TOKEN")
ukassa_secret_key = os.getenv("UKASSA_SECRET_KEY")
shop_id = os.getenv("SHOP_ID")

"""xlsx"""
xlsx_file_name = os.getenv("XLSX_FILE_NAME")
