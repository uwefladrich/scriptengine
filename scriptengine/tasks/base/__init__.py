""" ScriptEngine task handling and base tasks

Tasks are the basic units or work in ScriptEngine. A task serves a single,
specific limited purpose and should require a limited amount or work. Tasks
must have a well defined set of input parameters and be rather independent of
the execution context (e.g. parallel execution).

This module provides
  - the Task base class
  - the dynamic task loader
  - a set of basic tasks
"""

from .task import Task
from .loader import load, loaded_tasks

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


def task_loader_map():
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
