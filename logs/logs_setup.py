import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from colorama import Style
from nicelog.formatters import Colorful
from nicelog.styles.base import BaseStyle

from logs.logs_config import level_log, level_color, LOGGERS_CONFIG


class Filter(object):
    """Фильтр для обработчиков, для фильтрации высоких уровней логирования
        (Например, если уровень логирования стоит 10, то фильтр отсеивает все уровни выше 10)"""

    def __init__(self, level):
        self.__level = level

    def filter(self, logrecord):
        return logrecord.levelno <= self.__level


class LoggerStyle(BaseStyle):
    date = dict(fg='cyan')

    level_name_DEBUG = dict(fg='cyan', attrs=['reverse'])
    level_name_INFO = dict(fg='green')
    level_name_WARNING = dict(fg='yellow', attrs=['reverse'])
    level_name_ERROR = dict(fg='red', attrs=['reverse'])
    level_name_CRITICAL = dict(fg='red', attrs=['reverse'])
    level_name_DEFAULT = dict(fg='white', attrs=['reverse'])
    level_name_EVENT = dict(fg='hi_yellow')
    level_name_DAEMON = dict(bg='hi_red')

    logger_name = dict(fg='grey')
    file_name = dict(fg='green')
    line_number = dict(fg='hi_green')
    module_name = dict(fg='yellow')
    function_name = dict(fg='hi_yellow')

    message_DEBUG = dict(fg='cyan')
    message_INFO = dict(fg='green')
    message_WARNING = dict(fg='yellow')
    message_ERROR = dict(fg='red')
    message_CRITICAL = dict(fg='red')
    message_DEFAULT = dict(fg='white')

    exception = dict(fg='hi_grey')


def get_log_file_handler(formatter: logging.Formatter, level: str, logger_name: str) -> logging.FileHandler:
    """Функция для создания файлового обработчика.
        Получает готовый форматер, уровень логирования и имя логгера"""
    folder_name = os.path.join("logs", logger_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_name = os.path.join(folder_name, f"{level}.log")
    file_handler = RotatingFileHandler(file_name, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(level_log[level])
    file_handler.setFormatter(formatter)
    file_handler.addFilter(Filter(level_log[level]))
    return file_handler


def add_logging_level(level_name: str, level_num, method_name=None):
    """Функция для добавления нового уровня логирования"""

    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError('{} already defined in logging module'.format(level_name))
    if hasattr(logging, method_name):
        raise AttributeError('{} already defined in logging module'.format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError('{} already defined in logger class'.format(method_name))

    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)

    def log_to_root(message, *args, **kwargs):
        logging.log(level_num, message, *args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)


def configure_logger(logger_name, log_level):
    # Создание экземпляра логгера
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # Создание форматера
    date_format = '%Y-%m-%d %H:%M:%S'

    # Добавление обработчиков в логгер
    for level in level_log:
        log_format = f'%(asctime)s - [{Style.BRIGHT}{level_color[level]}%(levelname)s{Style.RESET_ALL}] - {Style.DIM}%(filename)s (%(funcName)s: line %(lineno)d){Style.RESET_ALL} - \n%(message)s'
        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
        logger.addHandler(get_log_file_handler(formatter, level, logger_name))

    # Добавление консольного обработчика
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(Colorful(style=LoggerStyle))
    logger.addHandler(stream_handler)

    return logger


def create_loggers(config):
    loggers = {}
    date_format = '%Y-%m-%d %H:%M:%S'
    for logger_config in config:
        logger_name = logger_config['name']
        log_level = logger_config['log_level']
        logger = configure_logger(logger_name, log_level)
        loggers[logger_name] = logger
        for level in level_log:
            log_format = f'%(asctime)s - [{Style.BRIGHT}{level_color[level]}%(levelname)s{Style.RESET_ALL}] - {Style.DIM}%(filename)s (%(funcName)s: line %(lineno)d){Style.RESET_ALL} - \n%(message)s'
            formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

            # добавляем уровень логирования, если его нет
            if not hasattr(logger, level):
                add_logging_level(level.upper(), level_log[level])
            logger.addHandler(get_log_file_handler(formatter, level, logger_name))
    return loggers


loggers = create_loggers(LOGGERS_CONFIG)
