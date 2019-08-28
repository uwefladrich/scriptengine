"""ScripteEngine helpers: Terminal Colors

Terminal markup and colors. To print colored text, use, for example:
print(terminal_colors.RED + "hello" + terminal_colors.RESET). For background
colors, use BG_ prefix, i.e. terminal_colors.BG_GREEN.
"""

# Resets all attributes
RESET = "\033[0m"

# Text markup
BOLD = "\033[01m"
DIM = "\033[02m"
UNDERLINE = "\033[04m"
REVERSE = "\033[07m"
STRIKETHROUGH = "\033[09m"
INVISIBLE = "\033[08m"

# Foreground colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
ORANGE = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
LIGHTGREY = "\033[37m"
DARKGREY = "\033[90m"
LIGHTRED = "\033[91m"
LIGHTGREEN = "\033[92m"
YELLOW = "\033[93m"
LIGHTBLUE = "\033[94m"
PINK = "\033[95m"
LIGHTCYAN = "\033[96m"

# Background colors
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_ORANGE = "\033[43m"
BG_BLUE = "\033[44m"
BG_PURPLE = "\033[45m"
BG_CYAN = "\033[46m"
BG_LIGHTGREY = "\033[47m"
