from django.apps import AppConfig


class TgBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tg_bot'
    verbose_name = 'телеграм бот'

    # def ready(self):
    #     # Регистрация команды приложения
    #     from .management.commands import mycommand