"""Getenv task for ScriptEngine."""

import os

from se.tasks import Task
from se.helpers import render_string


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
    def __init__(self, dictionary):
        super().__init__(__name__, dictionary, 'name', 'set_cfg')

    def __str__(self):
        return f'Get environment variable "{self.name}" and set "{self.set_cfg}" config'

    def run(self, **kwargs):
        self.log_info(f'{render_string(self.name, **kwargs)} '
                      f'--> {render_string(self.set_cfg, **kwargs)}')
        if getattr(kwargs, 'dryrun', False):
            print(render_string(str(self), **kwargs))
        else:
            env = os.environ.get(render_string(self.name, **kwargs))
            if env:
                return {render_string(self.set_cfg, **kwargs): env}
        return None
