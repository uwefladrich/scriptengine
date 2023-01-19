"""Getenv (base.getenv) and Setenv (base.setenv) tasks for ScriptEngine"""

import os

from scriptengine.context import ContextUpdate
from scriptengine.tasks.core import Task, timed_runner


class Getenv(Task):
    """Getenv task, reads environment variables.
    Getenv.run() takes the list of argument name, value pairs, reads the
    environment variables given by the argument values and stores the values of
    the environment variables as context parameters with the argument names.

    For example:
        base.getenv:
            home: HOME
            foo: BAR
    will store $HOME in context['home'] and $BAR in context['foo'].
    """

    @timed_runner
    def run(self, context):
        wanted = {
            n: self.getarg(n, context) for n in vars(self) if not n.startswith("_")
        }
        self.log_info(
            f"Read environment variables to context: {', '.join(wanted.values())}"
        )
        valid = {}
        for n, v in wanted.items():
            try:
                valid[n] = os.environ[v]
            except KeyError:
                self.log_warning(f"Environment variable {v} does not exist")
        return ContextUpdate(valid)


class Setenv(Task):
    """Setenv task, sets environment variables from context.
    Setenv.run() takes the list of argument name, value pairs, and sets the
    environemt variables given by the argument names to the values given by the
    argument values. For example,
        base.setenv:
            foo: one
            bar: 2
    will set $foo to "one" and $bar to "2".
    """

    @timed_runner
    def run(self, context):
        vars_ = {
            n: str(self.getarg(n, context)) for n in vars(self) if not n.startswith("_")
        }
        self.log_info(f'Set environment variables ({", ".join(vars_.keys())})')
        self.log_debug(vars_)
        os.environ.update(vars_)
