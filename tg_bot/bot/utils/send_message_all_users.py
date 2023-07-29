import asyncio
from aiogram.utils import exceptions as tg_exceptions

# from ..utils import setup_django_settings  # загрузка Django настроек
from tg_bot.bot.loader import bot
from tg_bot.bot.config import bot_logger
from tg_bot.models import Profile, TelegramMessage


# async def send_message_to_all_users(text_message: str):
async def send_message_to_all_users(model: TelegramMessage):
    """Рассылка сообщений в телеграм всем пользователям бота"""
    bot_logger.info("Запуск рассылки сообщений всем пользователям")
    text_message = model.text

    all_profiles = Profile.objects.all()  # список всех пользователей из базы данных
    try:
        for profile in all_profiles:
            # Отправляем сообщение каждому пользователю из списка
            await bot.send_message(chat_id=profile.tg_user_id, text=text_message)

    except tg_exceptions.BotBlocked:
        bot_logger.info("Bot is blocked by the user")
    except tg_exceptions.ChatNotFound:
        bot_logger.info("Chat not found")
    except tg_exceptions.RetryAfter as e:
        bot_logger.info(f"Retry in {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message_to_all_users(text_message)
    except tg_exceptions.UserDeactivated:
        bot_logger.info("User is deactivated")
    except tg_exceptions.TelegramAPIError:
        bot_logger.info("Telegram API error")

    model.send_status = True
    model.save()
