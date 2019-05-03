from jinja2 import Template
from distutils.util import strtobool


class TerminalColors(object):
    '''Terminal markup and colors To print colored text, use, for example:
    print(TerminalColor.RED + "hello" + TerminalColor.RESET)
    For background colors, use subclass BG, i.e. TerminalColors.BG.GREEN Bold,
    disable, underline, reverse, strikethrough, and invisible can be used from
    the main class.
    '''

    # Text markup
    RESET = '\033[0m'
    BOLD = '\033[01m'
    DIM = '\033[02m'
    UNDERLINE = '\033[04m'
    REVERSE = '\033[07m'
    STRIKETHROUGH = '\033[09m'
    INVISIBLE = '\033[08m'

    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    LIGHTGREY = '\033[37m'
    DARKGREY = '\033[90m'
    LIGHTRED = '\033[91m'
    LIGHTGREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHTBLUE = '\033[94m'
    PINK = '\033[95m'
    LIGHTCYAN = '\033[96m'

    # Background colors
    class BG:
        BLACK = '\033[40m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        ORANGE = '\033[43m'
        BLUE = '\033[44m'
        PURPLE = '\033[45m'
        CYAN = '\033[46m'
        LIGHTGREY = '\033[47m'


def render_string(string, **config):
    return Template(string).render(**config)


def render_string_recursive(string, **config):
    prev = string
    while True:
        curr = render_string(prev, **config)
        if curr != prev:
            prev = curr
        else:
            return curr


def eval_when_clause(string, **config):
    clause = ('{% if '
              + render_string_recursive(string, **config)
              + ' %}1{% else %}0{% endif %}')
    return bool(strtobool(render_string(clause, **config)))
