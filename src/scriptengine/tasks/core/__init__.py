""" ScriptEngine task handling

Tasks are the basic units or work in ScriptEngine. A task serves a single,
specific limited purpose and should require a limited amount or work. Tasks
must have a well defined set of input parameters and be rather independent of
the execution context (e.g. parallel execution).

This module provides
  - the Task base class
  - a timing wrapper for Task.run() functions
"""

from .task import Task
from .timing import timed_runner
