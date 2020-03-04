"""Getenv task for ScriptEngine."""

import os

from scriptengine.tasks import Task
from scriptengine.jinja import render as j2render


class Getenv(Task):
    """ Getenv task, reads environment variable

    The Getenv run() method reads an environmane variable and sets a
    ScriptEngine configuration parameter.

    Args:
        dictionary (dict): Must at least contain the following keys:
            - name: Name of the environment variable
            - set_cfg: Name of the ScriptEngine config parameter that is set to
                the value of the environment variable (if it exists)
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["name", "set_cfg"])

    def __str__(self):
        return f"Getenv: ENV{self.name} --> {self.set_cfg}"

    def run(self, context):
        self.log_info(f"ENV{self.name} --> {self.set_cfg}")
        env = os.environ.get(j2render(self.name, context))
        if env:
            context[j2render(self.set_cfg, context)] = env
