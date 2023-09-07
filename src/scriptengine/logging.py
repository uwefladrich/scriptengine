""" ScriptEngine logging.
"""

import logging
import logging.config

from scriptengine.helpers import terminal_colors as tc


class LogLevelFormatter:

    def __init__(self, formatters):
        self._formatters = formatters

    def format(self, record):
        return self._formatters[record.levelno].format(record)


def configure(log_level=logging.INFO):

    levels = [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ]

    colors = {
        logging.DEBUG: tc.CYAN,
        logging.INFO: tc.GREEN,
        logging.WARNING: tc.ORANGE,
        logging.ERROR: tc.RED,
        logging.CRITICAL: tc.RED,
    }

    formats = {
        'basic': {
            lvl: f'{colors[lvl]}{{asctime}} '
                 f'{tc.BOLD}{{levelname}}{tc.RESET}{colors[lvl]} '
                 f'[{{name}}] {{message}}'
                 f'{tc.RESET}'
            for lvl in levels
        },
        'with_id': {
            lvl: f'{colors[lvl]}{{asctime}} '
                 f'{tc.BOLD}{{levelname}}{tc.RESET}{colors[lvl]} '
                 f'[{{name}} <{{id}}>] {{message}}'
                 f'{tc.RESET}'
            for lvl in levels
        },
        'with_id_and_type': {
            lvl: f'{colors[lvl]}{{asctime}} '
                 f'{tc.BOLD}{{levelname}}{tc.RESET}{colors[lvl]} '
                 f'[{{name}}:{{type}} <{{id}}>] {{message}}'
                 f'{tc.RESET}'
            for lvl in levels
        },
    }

    date_format = '%Y-%m-%d %H:%M:%S'

    configuration = dict(

        version=1,

        formatters={
            'basic': {
                '()': 'scriptengine.logging.LogLevelFormatter',
                'formatters': {
                    lvl: logging.Formatter(
                            fmt=formats['basic'][lvl],
                            style='{',
                            datefmt=date_format
                         )
                    for lvl in levels
                }
            },
            'job': {
                '()': 'scriptengine.logging.LogLevelFormatter',
                'formatters': {
                    lvl: logging.Formatter(
                            fmt=formats['with_id'][lvl],
                            style='{',
                            datefmt=date_format
                         )
                    for lvl in levels
                }
            },
            'task': {
                '()': 'scriptengine.logging.LogLevelFormatter',
                'formatters': {
                    lvl: logging.Formatter(
                            fmt=formats['with_id_and_type'][lvl],
                            style='{',
                            datefmt=date_format
                         )
                    for lvl in levels
                }
            },
        },

        handlers={
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'basic',
                },
            'job': {
                'class': 'logging.StreamHandler',
                'formatter': 'job',
                },
            'task': {
                'class': 'logging.StreamHandler',
                'formatter': 'task',
                },
        },

        loggers={
            'se': {
                'handlers': ['default'],
                'level': log_level,
            },
            'se.job': {
                'handlers': ['job'],
                'level': log_level,
                'propagate': False,
            },
            'se.task': {
                'handlers': ['task'],
                'level': log_level,
                'propagate': False,
            },
            'se.task.loader': {
                'handlers': ['default'],
                'level': log_level,
                'propagate': False,
            },
        },
    )
    logging.config.dictConfig(configuration)
