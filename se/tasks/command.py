"""Command task for ScriptEngine."""

import ast
import subprocess

from se.tasks import Task
from se.helpers import render_string


class Command(Task):
    """Command task, executes a command in a shell.
    """
    def __init__(self, dictionary):
        super().__init__(__name__, dictionary, 'name')

    def __str__(self):
        return f'Command "{self.name}" with args "{getattr(self, "args", None)}"'

    def run(self, **kwargs):
        self.log_info(f'{render_string(self.name, **kwargs)} '
                      f'{render_string(str(getattr(self, "args", "")), **kwargs)}')

        if getattr(kwargs, 'dryrun', False):
            print(render_string(str(self), **kwargs))
        else:
            command = render_string(self.name, **kwargs)
            arglist = getattr(self, 'args', [])
            if isinstance(arglist, str):
                try:
                    arglist = ast.literal_eval(render_string(arglist, **kwargs)) or []
                except ValueError:
                    raise RuntimeError(f'Command task: can''t parse "args": {arglist!s}')
            else:
                try:
                    arglist = [render_string(arg, **kwargs) for arg in arglist]
                except TypeError:
                    raise RuntimeError(f'Command task: "args" not iterable: {arglist!s}')
            cwd = render_string(self.cwd, **kwargs) if hasattr(self, 'cwd') else None
            subprocess.run([command]+arglist, cwd=cwd)
