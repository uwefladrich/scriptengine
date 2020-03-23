""" ScriptEngine base tasks

This module provides basic SE tasks.
"""

from .include import Include
from .config import Config
from .echo import Echo
from .chdir import Chdir
from .command import Command
from .getenv import Getenv
from .exit import Exit
from .file import Copy, Move, Link, Remove, MakeDir
from .find import Find
from .template import Template


def taskmap():
    return {'include': Include,
            'config': Config,
            'echo': Echo,
            'chdir': Chdir,
            'command': Command,
            'getenv': Getenv,
            'exit': Exit,
            'copy': Copy,
            'move': Move,
            'link': Link,
            'remove': Remove,
            'make_dir': MakeDir,
            'find': Find,
            'template': Template}
