"""ScripteEngine helpers: Colored terminal output

Terminal markup and colors by using ANSI escape sequences. To print colored
text, use, for example:

    import terminal_colors as TC

    print(f'{TC.RED}Hello!{TC.RESET}')

For background colors, use BG_ prefix, i.e. TC.BG_GREEN.

The module supports color themes. To set another theme, use, for example

    TC.set_theme('none')

Further output will then be without colors.
"""

import sys

from scriptengine.exceptions import ScriptEngineError

# The default color theme
ACTIVE_THEME = 'standard'

# All themes with all colors.
# It is not necessary that all themes define the same colors. But if you are
# using a color that is not defined in the active theme, there will be an
# AttributeError.
COLORTABLE = {
    'standard': {
        'RESET': '\033[0m',

        'BOLD': '\033[01m', 'DIM': '\033[02m', 'UNDERLINE': '\033[04m',
        'REVERSE': '\033[07m', 'STRIKETHROUGH': '\033[09m',
        'INVISIBLE': '\033[08m',

        'BLACK': '\033[30m', 'RED': '\033[31m', 'GREEN': '\033[32m',
        'ORANGE': '\033[33m', 'BLUE': '\033[34m', 'PURPLE': '\033[35m',
        'CYAN': '\033[36m', 'LIGHTGREY': '\033[37m', 'DARKGREY': '\033[90m',
        'LIGHTRED': '\033[91m', 'LIGHTGREEN': '\033[92m',
        'YELLOW': '\033[93m', 'LIGHTBLUE': '\033[94m', 'PINK': '\033[95m',
        'LIGHTCYAN': '\033[96m',

        'BG_BLACK': '\033[40m', 'BG_RED': '\033[41m', 'BG_GREEN': '\033[42m',
        'BG_ORANGE': '\033[43m', 'BG_BLUE': '\033[44m',
        'BG_PURPLE': '\033[45m', 'BG_CYAN': '\033[46m',
        'BG_LIGHTGREY': '\033[47m'},

    'none': {
        'RESET': '',

        'BOLD': '', 'DIM': '', 'UNDERLINE': '', 'REVERSE': '',
        'STRIKETHROUGH': '', 'INVISIBLE': '',

        'BLACK': '', 'RED': '', 'GREEN': '', 'ORANGE': '',
        'BLUE': '', 'PURPLE': '', 'CYAN': '', 'LIGHTGREY': '',
        'DARKGREY': '', 'LIGHTRED': '', 'LIGHTGREEN': '',
        'YELLOW': '', 'LIGHTBLUE': '', 'PINK': '',
        'LIGHTCYAN': '',

        'BG_BLACK': '', 'BG_RED': '', 'BG_GREEN': '',
        'BG_ORANGE': '', 'BG_BLUE': '', 'BG_PURPLE': '',
        'BG_CYAN': '', 'BG_LIGHTGREY': ''}
    }


def set_theme(theme):
    """ Changes the active color theme
    """
    global ACTIVE_THEME
    if theme not in COLORTABLE.keys():
        raise ScriptEngineError(f'Invalid terminal color scheme: "{theme}"')
    ACTIVE_THEME = theme

    # Clean all present color settings
    for color in {c for t in COLORTABLE for c in COLORTABLE[t]}:
        if hasattr(sys.modules[__name__], color):
            delattr(sys.modules[__name__], color)

    # Set colors for new theme
    for color, value in COLORTABLE[theme].items():
        setattr(sys.modules[__name__], color, value)


# Set default colors
for _color, _value in COLORTABLE[ACTIVE_THEME].items():
    setattr(sys.modules[__name__], _color, _value)
