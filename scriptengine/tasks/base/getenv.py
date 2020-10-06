"""Getenv task for ScriptEngine."""

import os

from scriptengine.tasks.base import Task
from scriptengine.tasks.base.timing import timed_runner


class Getenv(Task):
    """ Getenv task, reads environment variable

    The Getenv run() method reads an environmane variable and sets a
    ScriptEngine configuration parameter.

    Args:
        dictionary (dict): Must at least contain the following keys:
            - name: Name of the environment variable
            - set: Name of the ScriptEngine config parameter that is set to
                the value of the environment variable (if it exists)
    """
    _required_arguments = ('name', 'set', )

    def __init__(self, arguments):
        Getenv.check_arguments(arguments)
        super().__init__(arguments)

    def __str__(self):
        return f"Getenv: ENV{self.name} --> {self.set}"

    @timed_runner
    def run(self, context):
        self.log_info(f"ENV{self.name} --> {self.set}")
        env = os.environ.get(self.getarg('name', context))
        if env:
            context[self.getarg('set', context)] = env
