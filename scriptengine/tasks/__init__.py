"""ScriptEngine tasks.

Tasks are the basic units or work in ScriptEngine. A task serves a single,
specific limited purpose and should require a limited amount or work. Tasks
must have a well defined set of input parameters and be rather independent of
the execution context (e.g. parallel execution).

This module provides the Task base class and the dynamic task loader.
ScriptEngine base tasks are in the base submodule.
"""

from .task import Task
from .loader import load, loaded
