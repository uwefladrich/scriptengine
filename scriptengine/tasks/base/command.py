"""Command task for ScriptEngine

   Example:
      - command:
            name: ls
            args: [-l, -a]
"""

import subprocess
import threading
import os
from contextlib import contextmanager

from scriptengine.tasks.core import Task, timed_runner
from scriptengine.exceptions import (
    ScriptEngineTaskRunError,
    ScriptEngineTaskArgumentInvalidError,
)


class LogPipe(threading.Thread):
    """Helper class that can be used in the subprocess.run() call as argument
    for stdout and stderr. It implements a pipe that sends whatever it receives
    to a log function (provided at initialisation). This can be used to send
    stdout/stderr of a subprocess to a logger.
    Follows https://codereview.stackexchange.com/questions/6567"""

    def __init__(self, log_function):
        super().__init__()
        self.log_function = log_function
        self.fd_read, self.fd_write = os.pipe()
        self.pipe_reader = os.fdopen(self.fd_read)
        self.start()

    def fileno(self):
        return self.fd_write

    def run(self):
        for line in iter(self.pipe_reader.readline, ""):
            self.log_function(line.strip("\n"))
        self.pipe_reader.close()

    def close(self):
        os.close(self.fd_write)


class Command(Task):
    """Command task, executes a command in a shell"""

    _required_arguments = ("name",)

    def __init__(self, arguments):
        Command.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        self.log_info(
            f"{self.name} "
            f'args={getattr(self, "args", None)} '
            f'cwd={getattr(self, "cwd", None)}'
        )

        command = self.getarg("name", context)

        args = self.getarg("args", context, default=[])
        args = args if isinstance(args, list) else [args]

        cwd = self.getarg("cwd", context, default=None)
        ignore_error = self.getarg("ignore_error", context, default=False)

        self.log_debug(
            f"{command} "
            f'{" ".join(map(str, args))} '
            f"cwd={cwd} "
            f"ignore_error={ignore_error} "
        )

        @contextmanager
        def log_pipe(mode):
            """Returns something that can be used as stdout/stderr argument for
            subprocess.run(). If mode is True, a LogPipe is returned, which
            sends stdout/stderr through the info logger of the tasks. If mode is
            None/False, then None is returned and stdout/stderr are ignored. If
            mode is a string, stdout/stderr is captured by subprocess and later
            stored in the context."""
            if mode is True:
                pipe = LogPipe(self.log_info)
            elif not mode:
                pipe = None
            elif isinstance(mode, str):
                pipe = subprocess.PIPE
            else:
                self.log_error(f"Invalid task argument: {mode}")
                raise ScriptEngineTaskArgumentInvalidError
            try:
                yield pipe
            finally:
                if isinstance(pipe, LogPipe):
                    pipe.close()

        stdout_mode = self.getarg("stdout", context, default=True)
        self.log_debug(
            "stdout mode: "
            f'{stdout_mode if stdout_mode in (True, False) else "context"}'
        )
        stderr_mode = self.getarg("stderr", context, default=True)
        self.log_debug(
            "stderr mode: "
            f'{stderr_mode if stderr_mode in (True, False) else "context"}'
        )
        with log_pipe(stdout_mode) as stdout, log_pipe(stderr_mode) as stderr:
            try:
                cmd_proc = subprocess.run(
                    map(str, (command, *args)),
                    stdout=stdout,
                    stderr=stderr,
                    cwd=cwd,
                    check=True,
                    errors="replace",
                )
            except subprocess.CalledProcessError as e:
                if ignore_error:
                    self.log_warning(f"Command returned error code {e.returncode}")
                else:
                    self.log_error(f"Command returned error code {e.returncode}")
                    raise ScriptEngineTaskRunError
            else:
                if isinstance(stdout_mode, str):
                    context[stdout_mode] = cmd_proc.stdout.split("\n")
                if isinstance(stderr_mode, str):
                    context[stderr_mode] = cmd_proc.stderr.split("\n")
