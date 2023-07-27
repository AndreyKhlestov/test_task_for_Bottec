import logging
from colorama import Fore

# Настройка приоритетов для уровней логирования
level_log = {
    'debug': 10,
    'daemon': 15,
    'info': 20,
    'warning': 30,
    'error_pay': 31,
    'error': 40,
    'exception': 50,
}

# Настройка цветов для уровней логирования
level_color = {
    'debug': Fore.WHITE,
    'daemon': 15,
    'info': Fore.GREEN,
    'warning': Fore.YELLOW,
    'error_pay': Fore.CYAN,
    'error': Fore.MAGENTA,
    'exception': Fore.RED,
}

# Названия логеров и уровень отображения
LOGGERS_CONFIG = [
    # {'name': 'ServerLogger', 'log_level': logging.DEBUG},
    {'name': 'BotLogger', 'log_level': logging.DEBUG},
    # {'name': 'AnotherLogger', 'log_level': logging.DEBUG},
]
