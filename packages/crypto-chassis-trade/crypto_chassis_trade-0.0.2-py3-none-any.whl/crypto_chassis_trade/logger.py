import logging
import os
import sys
import time
from enum import IntEnum
from inspect import getframeinfo, stack
from logging.config import fileConfig

# import time
# import random
# log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
# logging.config.fileConfig(log_file_path)

# class Logger:


class LogLevel(IntEnum):
    TRACE = 1
    DEBUG = 2
    DETAIL = 3
    INFO = 4
    WARNING = 5
    ERROR = 6
    CRITICAL = 7
    NONE = 8


fileConfig(os.path.dirname(os.path.realpath(__file__)) + "/logger_config.ini")
logging.Formatter.converter = time.gmtime
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
message_format = "{{{}:{}:{}}} {}"
#
#     def getLogger(cls):
#
#         return logging.getLogger()
level = LogLevel.INFO

seperator = "\n"


def set_level(level_to_set: LogLevel):
    global level
    level = level_to_set


def setLevel(levelToSet: LogLevel):
    set_level(levelToSet)


def trace(*messages):
    if level <= LogLevel.TRACE:
        this_function = getframeinfo(stack()[0][0])
        caller = getframeinfo(stack()[1][0])
        logger.debug(
            message_format.format(
                os.path.basename(caller.filename), caller.function, caller.lineno, f"{this_function.function}{10*' '}{seperator.join(messages)}\n"
            )
        )


def debug(*messages):
    if level <= LogLevel.DEBUG:
        this_function = getframeinfo(stack()[0][0])
        caller = getframeinfo(stack()[1][0])
        logger.debug(
            message_format.format(
                os.path.basename(caller.filename), caller.function, caller.lineno, f"{this_function.function}{10*' '}{seperator.join(messages)}\n"
            )
        )


def detail(*messages):
    if level <= LogLevel.DETAIL:
        this_function = getframeinfo(stack()[0][0])
        caller = getframeinfo(stack()[1][0])
        logger.info(
            message_format.format(
                os.path.basename(caller.filename), caller.function, caller.lineno, f"{this_function.function}{10*' '}{seperator.join(messages)}\n"
            )
        )


def info(*messages):
    if level <= LogLevel.INFO:
        this_function = getframeinfo(stack()[0][0])
        caller = getframeinfo(stack()[1][0])
        logger.info(
            message_format.format(
                os.path.basename(caller.filename), caller.function, caller.lineno, f"{this_function.function}{10*' '}{seperator.join(messages)}\n"
            )
        )


def warning(*messages):
    if level <= LogLevel.WARNING:
        this_function = getframeinfo(stack()[0][0])
        caller = getframeinfo(stack()[1][0])
        logger.warning(
            message_format.format(
                os.path.basename(caller.filename), caller.function, caller.lineno, f"{this_function.function}{10*' '}{seperator.join(messages)}\n"
            )
        )


def error(*messages):
    if level <= LogLevel.ERROR:
        this_function = getframeinfo(stack()[0][0])
        caller = getframeinfo(stack()[1][0])
        if len(messages) == 1 and isinstance(messages[0], Exception):
            logger.error(
                message_format.format(os.path.basename(caller.filename), caller.function, caller.lineno, f"{this_function.function}{10*' '}{messages[0]}\n"),
                exc_info=messages[0],
            )
        else:
            logger.warning(
                message_format.format(
                    os.path.basename(caller.filename), caller.function, caller.lineno, f"{this_function.function}{10*' '}{seperator.join(messages)}\n"
                )
            )


def critical(*messages):
    if level <= LogLevel.CRITICAL:
        this_function = getframeinfo(stack()[0][0])
        caller = getframeinfo(stack()[1][0])
        if len(messages) == 1 and isinstance(messages[0], Exception):
            logger.critical(
                message_format.format(os.path.basename(caller.filename), caller.function, caller.lineno, f"{this_function.function}{10*' '}{messages[0]}\n"),
                exc_info=messages[0],
            )
        else:
            logger.warning(
                message_format.format(
                    os.path.basename(caller.filename), caller.function, caller.lineno, f"{this_function.function}{10*' '}{seperator.join(messages)}\n"
                )
            )
        sys.exit(1)
