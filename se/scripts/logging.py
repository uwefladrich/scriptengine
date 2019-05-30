import logging

from se.helpers import TerminalColors as TC

class DispatchingFormatter:
    """Dispatch formatter for logger and it's sub logger."""
    def __init__(self, formatters, default_formatter):
        self._formatters = formatters
        self._default_formatter = default_formatter

    def format(self, record):
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

def log_formatter(color=None):
    if color:
        format_string = '%(asctime)s {}%(levelname)s [%(name)s]: {}%(message)s{}'.format(color+TC.BOLD, TC.RESET+color, TC.RESET)
    else:
        format_string = '%(asctime)s %(levelname)s [%(name)s] %(message)s'

    return logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S')

def app_logger(name, level=logging.INFO):
    """ Returns a Logger
    """
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(DispatchingFormatter({
            logging.DEBUG:   log_formatter(TC.CYAN),
            logging.INFO:    log_formatter(TC.GREEN),
            logging.WARNING: log_formatter(TC.ORANGE),
            logging.ERROR:   log_formatter(TC.RED),
        },
        log_formatter(TC.BLUE),
    ))
    logger = logging.getLogger(name)
    logger.addHandler(stdout_handler)
    logger.setLevel(level)

    return logger
