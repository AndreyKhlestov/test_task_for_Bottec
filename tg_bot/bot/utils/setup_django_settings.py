import os
import django

# Устанавливаем переменные окружения DJANGO_SETTINGS_MODULE для указания пути до settings.py Django проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_Django.bot_Django.settings')
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
django.setup()
