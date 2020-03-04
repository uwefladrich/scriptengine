"""Command task for ScriptEngine

   Example:
      - command:
            name: ls
            args: [-l, -a]
"""

import ast
import subprocess

from scriptengine.tasks import Task
from scriptengine.jinja import render as j2render
from scriptengine.exceptions import ScriptEngineStopException


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

        command = j2render(self.name, context)

        args = j2render(str(getattr(self, "args", "")), context) or "[]"
        try:
            args = ast.literal_eval(args)
        except ValueError:
            args = ast.literal_eval(f'"{args}"')
        args = args if isinstance(args, list) else [args]

        cwd = j2render(getattr(self, "cwd", ''), context) or None

        self.log_debug(f"{command} {' '.join(map(str,args))}"
                       f"{' cwd='+cwd if cwd else ''}")

        stdout = getattr(self, "stdout", None)
        try:
            result = subprocess.run(map(str, [command]+args),
                                    stdout=subprocess.PIPE if stdout is not None else None,
                                    cwd=cwd,
                                    check=True)
        except subprocess.CalledProcessError as error:
            if getattr(self, "ignore_error", False) is True:
                self.log_warning(f"{self.name} returned error code {error.returncode}")
            else:
                self.log_error(f"{self.name} returned error code {error.returncode}")
                raise ScriptEngineStopException("Stopping ScriptEngine after nonzero "
                                                "exit code in command task")
        else:
            if stdout is not None:
                context[stdout] = [binary.decode("UTF-8") for binary in result.stdout.splitlines()]
