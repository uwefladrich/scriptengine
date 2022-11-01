"""ScriptEngine file tasks
Provides Copy, Move, Link, Remove and MakeDir tasks
"""

import pathlib
import shutil

from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.tasks.core import Task, timed_runner


def _getarg_path(self, name, context={}, **kwargs):
    """Wrapper for Task.getarg() that returns a pathlib.Path"""
    arg = self.getarg(name, context, **kwargs)
    try:
        return pathlib.Path(arg)
    except TypeError:
        self.log_error(f'Invalid "{name}" argument, "{arg}" is not a path')
        raise ScriptEngineTaskRunError
