"""ScriptEngine tasks.

Tasks are the basic units or work in ScriptEngine. A task serves a single,
specific limited purpose and should require a limited amount or work. Tasks
must have a well defined set of input parameters and be rather independent of
the execution context (e.g. parallel execution).

This module provides the base class as well as derived classes for specific
tasks.
"""

from .task import Task

from .config import Config
from .echo import Echo
from .file import Copy, Move, Link, Remove, MakeDir
from .command import Command
from .template import Template
from .getenv import Getenv
from .include import Include
from .exit import Exit
from .chdir import Chdir
from .slurm_submit import SlurmSubmit
from .eceinfo import UpdateEceinfo, WriteEceinfo
