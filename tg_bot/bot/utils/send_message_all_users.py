import asyncio
from aiogram.utils import exceptions as tg_exceptions

from tg_bot.bot.loader import bot
from tg_bot.bot.config import bot_logger
from tg_bot.models import Profile, TelegramMessage


async def send_message_to_all_users():
    print("send_message_to_all_users")
    while True:
        # получаем неотправленные рассылки
        new_mailing = TelegramMessage.objects.filter(send_status=False).order_by('start_date_time')

        if new_mailing:
            all_profiles = Profile.objects.all()  # список всех пользователей из базы данных
            for mailing in new_mailing:
                for profile in all_profiles:
                    try:
                        await bot.send_message(chat_id=profile.tg_user_id, text=mailing.text)  # Отправляем сообщение
                    except tg_exceptions.BotBlocked:
                        bot_logger.info("Bot is blocked by the user")
                    except tg_exceptions.ChatNotFound:
                        bot_logger.info("Chat not found")
                    except tg_exceptions.RetryAfter as e:
                        bot_logger.info(f"Retry in {e.timeout} seconds.")
                        await asyncio.sleep(e.timeout)
                        await bot.send_message(chat_id=profile.tg_user_id, text=mailing.text)
                    except tg_exceptions.UserDeactivated:
                        bot_logger.info("User is deactivated")
                    except tg_exceptions.TelegramAPIError:
                        bot_logger.info("Telegram API error")

                # После отправки рассылки изменяем ее статус
                mailing.send_status = True
                mailing.save()

        await asyncio.sleep(1)  # Проверка каждую секунду
