""" ScriptEngine logging.
"""

import logging

from scriptengine.helpers import terminal_colors as tc


_DATEFMT = '%Y-%m-%d %H:%M:%S'


class DispatchingFormatter:
    """Inspired by https://stackoverflow.com/questions/1741972
    """
    def __init__(self, formatters, default_formatter):
        self._formatters = formatters
        self._default_formatter = default_formatter

    def format(self, record):
        formatter = self._formatters.get(record.levelno,
                                         self._default_formatter)
        return formatter.format(record)


def configure_logger(name, level, formatter):
    handler = logging.StreamHandler()
    handler.setFormatter(DispatchingFormatter({
        logging.DEBUG: formatter(tc.CYAN),
        logging.INFO: formatter(tc.GREEN),
        logging.WARNING: formatter(tc.ORANGE),
        logging.ERROR: formatter(tc.RED),
        logging.CRITICAL: formatter(tc.RED),
        },
        formatter('')
    ))
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)


def cli_log_formatter(color):
    fmt = (f'{{asctime}} {color+tc.BOLD}{{levelname}}'
           f' [{{name}}]{tc.RESET+color} {{message}}{tc.RESET}')
    return logging.Formatter(fmt, style='{', datefmt=_DATEFMT)


def task_log_formatter(color):
    fmt = (f'{{asctime}} {color+tc.BOLD}{{levelname}}'
           f' [{{name}} <{{id}}>]{tc.RESET+color} {{message}}{tc.RESET}')
    return logging.Formatter(fmt, style='{', datefmt=_DATEFMT)
