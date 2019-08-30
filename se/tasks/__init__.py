"""ScriptEngine tasks.

Tasks are the basic units or work in ScriptEngine. A task serves a single,
specific limited purpose and should require a limited amount or work. Tasks
must have a well defined set of input parameters and be rather independent of
the execution context (e.g. parallel execution).

This module provides the base class as well as derived classes for specific
tasks.
"""

from se.tasks.task import Task
from se.tasks.config import Config
from se.tasks.echo import Echo
from se.tasks.copy import Copy
from se.tasks.command import Command
from se.tasks.template import Template
from se.tasks.getenv import Getenv
from se.tasks.include import Include
