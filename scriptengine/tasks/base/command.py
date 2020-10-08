"""Command task for ScriptEngine

   Example:
      - command:
            name: ls
            args: [-l, -a]
"""

import subprocess

from scriptengine.tasks.base import Task
from scriptengine.tasks.base.timing import timed_runner
from scriptengine.exceptions import ScriptEngineTaskRunError


class Command(Task):
    """Command task, executes a command in a shell"""

    _required_arguments = ('name', )

    def __init__(self, arguments):
        Command.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        self.log_info(f"{self.name} "
                      f"args={getattr(self, 'args', 'none')} "
                      f"cwd={getattr(self, 'cwd', 'none')}")

        command = self.getarg('name', context)

        args = self.getarg('args', context, default=[])
        args = args if isinstance(args, list) else [args]

        cwd = self.getarg('cwd', context, default=None)

        self.log_debug(f"{command} {' '.join(map(str,args))}"
                       f"{' cwd='+cwd if cwd else ''}")

        stdout = self.getarg('stdout', default=None)
        try:
            result = subprocess.run(
                        map(str, [command]+args),
                        stdout=subprocess.PIPE if stdout is not None else None,
                        cwd=cwd,
                        check=True)
        except subprocess.CalledProcessError as error:
            msg = (f'Command "{self.name}" returned '
                   f'error code {error.returncode}')
            if self.getarg('ignore_error', context, default=False):
                self.log_warning(msg)
            else:
                self.log_error(msg)
                raise ScriptEngineTaskRunError(msg)
        else:
            if stdout is not None:
                context[stdout] = [binary.decode("UTF-8")
                                   for binary in result.stdout.splitlines()]
