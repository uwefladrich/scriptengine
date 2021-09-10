"""Command task for ScriptEngine

   Example:
      - command:
            name: ls
            args: [-l, -a]
"""

import subprocess

from scriptengine.tasks.core import Task, timed_runner
from scriptengine.exceptions import ScriptEngineTaskRunError, \
                                    ScriptEngineTaskArgumentInvalidError


class Command(Task):
    """Command task, executes a command in a shell"""

    _required_arguments = ('name', )

    def __init__(self, arguments):
        Command.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        self.log_info(
            f'{self.name} '
            f'args={getattr(self, "args", None)} '
            f'cwd={getattr(self, "cwd", None)}'
        )

        command = self.getarg('name', context)

        args = self.getarg('args', context, default=[])
        args = args if isinstance(args, list) else [args]

        cwd = self.getarg('cwd', context, default=None)
        stdout = self.getarg('stdout', context, default=True)
        ignore_error = self.getarg('ignore_error', context, default=False)

        self.log_debug(
            f'\"{command} {" ".join(map(str, args))}\" '
            f'cwd={cwd} stdout={stdout} ignore_error={ignore_error}'
        )

        try:
            cmd_proc = subprocess.run(
                map(str, (command, *args)),
                capture_output=True,
                cwd=cwd,
                check=True,
            )
        except subprocess.CalledProcessError as error:
            err_msg = (
                f'Command "{command}" returned error code '
                f'{error.returncode} (error message below)\n'
            )
            err_msg += '\n'.join(error.stderr.decode('UTF-8').splitlines())
            if ignore_error:
                self.log_warning(err_msg)
                self.log_warning(
                    'The error is ignored because "ignore_error" is true'
                )
            else:
                self.log_error(err_msg)
                raise ScriptEngineTaskRunError
        else:
            if stdout not in (False, None):
                stdout_lines = cmd_proc.stdout.decode('UTF-8').splitlines()
                if stdout is True:
                    self.log_info(
                        'Command "{command}" output follows below:\n'
                        + '\n'.join(stdout_lines)
                    )
                elif isinstance(stdout, str):
                    context[stdout] = stdout_lines
                else:
                    self.log_error(
                       'Invalid type for "stdout" argument (should be str): '
                       f'{stdout} has type {type(stdout).__name__}'
                    )
                    raise ScriptEngineTaskArgumentInvalidError
