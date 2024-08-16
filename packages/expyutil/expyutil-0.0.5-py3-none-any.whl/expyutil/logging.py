#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import os
import logging
import logging.handlers
from datetime import datetime

LEVEL_COLOR = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}
STDOUT_LOG_FMT = "%(log_color)s[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
STDOUT_DATE_FMT = "%y-%m-%d %H:%M:%S"
FILE_LOG_FMT = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
FILE_DATE_FMT = "%y-%m-%d %H:%M:%S"


class ColoredFormatter(logging.Formatter):

    COLOR_MAP = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
        "bg_black": "40",
        "bg_red": "41",
        "bg_green": "42",
        "bg_yellow": "43",
        "bg_blue": "44",
        "bg_magenta": "45",
        "bg_cyan": "46",
        "bg_white": "47",
        "light_black": "1;30",
        "light_red": "1;31",
        "light_green": "1;32",
        "light_yellow": "1;33",
        "light_blue": "1;34",
        "light_magenta": "1;35",
        "light_cyan": "1;36",
        "light_white": "1;37",
        "light_bg_black": "100",
        "light_bg_red": "101",
        "light_bg_green": "102",
        "light_bg_yellow": "103",
        "light_bg_blue": "104",
        "light_bg_magenta": "105",
        "light_bg_cyan": "106",
        "light_bg_white": "107",
    }

    def __init__(self, fmt, datefmt):
        super(ColoredFormatter, self).__init__(fmt, datefmt)

    def parse_color(self, level_name):
        color_name = LEVEL_COLOR.get(level_name, "")
        if not color_name:
            return ""

        color_value = []
        color_name = color_name.split(",")
        for _cn in color_name:
            color_code = self.COLOR_MAP.get(_cn, "")
            if color_code:
                color_value.append(color_code)

        return "\033[" + ";".join(color_value) + "m"


    def format(self, record):
        record.log_color = self.parse_color(record.levelname)
        message = super(ColoredFormatter, self).format(record) + "\033[0m"

        return message


default_color_fmter = ColoredFormatter(
    fmt=STDOUT_LOG_FMT,
    datefmt=STDOUT_DATE_FMT,
)

def setup_logger(name, log_level="debug", path=None, clear=True):
    """
    log_level can be upper case or lower case
    """

    _logger = logging.getLogger(name)
    if clear:
        _logger.handlers.clear()    # clear all exist handlers

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(default_color_fmter)
    _logger.addHandler(stdout_handler)

    if not path is None:
        add_file_handler(_logger, path)

    _logger.setLevel(log_level.upper())
    return _logger

def add_file_handler(logger, path, file_handler=None):
    base_dir = os.path.dirname(path)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(base_dir)
    if file_handler is None:
        file_handler = logging.FileHandler(path)
    file_formatter = logging.Formatter(
        fmt=FILE_LOG_FMT,
        datefmt=FILE_DATE_FMT,
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

def all_loggers_names():

    root_logger = logging.getLogger()
    all_loggers = root_logger.manager.loggerDict.keys()
    return list(all_loggers)

def get_strftime():
    return datetime.now().strftime("%y-%m-%d-%H-%M-%S")