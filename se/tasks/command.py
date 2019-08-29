"""Command task for ScriptEngine

   Example:
      - command:
            name: ls
            args: [-l, -a]
"""

import ast
import subprocess

from se.tasks import Task
from se.helpers import render_string


class Command(Task):
    """Command task, executes a command in a shell"""
    def __init__(self, parameters):
        super().__init__(__name__, parameters, ["name"])

    def __str__(self):
        return f"Command: {self.name} {getattr(self, 'args', '')}"

    def run(self, context):
        self.log_info(f"{self.name} "
                      f"args={getattr(self, 'args', 'none')} "
                      f"cwd={getattr(self, 'cwd', 'none')}")

        command = render_string(self.name, context)

        args = render_string(str(getattr(self, "args", "")), context) or "[]"
        try:
            args = ast.literal_eval(args)
        except ValueError:
            args = ast.literal_eval(f'"{args}"')
        args = args if isinstance(args, list) else [args]

        cwd = render_string(getattr(self, "cwd", ''), context) or None

        self.log_debug(f"{command} {' '.join(map(str,args))}"
                       f"{' cwd='+cwd if cwd else ''}")

        subprocess.run(map(str, [command]+args), cwd=cwd)
