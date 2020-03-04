""" ScriptEngine logging.
"""

import logging

from scriptengine.helpers import terminal_colors as tc

class DispatchingFormatter:
    """Dispatch formatter for logger and it's sub logger."""
    def __init__(self, formatters, default_formatter):
        self._formatters = formatters
        self._default_formatter = default_formatter

    def format(self, record):
        """Searches among self._formatters for the formatter with matching
        record.levelno and applies formatter to record.

        Args:
            record: the logging record

        Returns:
            the logging record formatted with chosen formatter
        """
        # Search from record's logger up to it's parents:
        logger = logging.getLogger(record.name)
        while logger:
            # Check if suitable formatter for current logger exists:
            if record.levelno in self._formatters:
                formatter = self._formatters[record.levelno]
                break
            else:
                logger = logger.parent
        else:
            # If no formatter found, just use default:
            formatter = self._default_formatter
        return formatter.format(record)

def _log_formatter(color=None):
    """Sets the format string and returns a logging.Formatter object.
    Args:
        color: a color value from scriptengine.helpers.terminal_colors

    Returns:
        a logging.Formatter object
    """
    if color:
        format_string = (f"%(asctime)s {color+tc.BOLD}%(levelname)s [%(name)s]: "
                         f"{tc.RESET+color}%(message)s{tc.RESET}")
    else:
        format_string = "%(asctime)s %(levelname)s [%(name)s] %(message)s"

    return logging.Formatter(format_string, datefmt="%Y-%m-%d %H:%M:%S")

def logger(name, level=logging.INFO):
    """ Returns a Logger

    Args:
        name (str): The logger name. Use class name for ScriptEngine modules.
        level: a logging level (one of logging.DEBUG, logging.INFO,
            logging.WARNING, logging.ERROR)
    Returns:
        the logger
    """
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(DispatchingFormatter(
        {
            logging.DEBUG:   _log_formatter(tc.CYAN),
            logging.INFO:    _log_formatter(tc.GREEN),
            logging.WARNING: _log_formatter(tc.ORANGE),
            logging.ERROR:   _log_formatter(tc.RED),
        },
        _log_formatter(tc.BLUE),
    ))
    logger = logging.getLogger(name)
    logger.addHandler(stdout_handler)
    logger.setLevel(level)

    return logger
