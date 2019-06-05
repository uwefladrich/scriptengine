"""Configuration task for ScriptEngine."""

from se.tasks import Task
from se.helpers import render_string


class Configuration(Task):
    """Configuration task, sets configuration parameters.

    The tasks run() method returns all name-value pairs passed at creation time
    in a dict.
    """
    def __init__(self, dictionary):
        super().__init__(__name__, dictionary)

    def __str__(self):
        return f'Configuration: {self.__dict__}'

    def run(self, **kwargs):
        config = {key:val for key, val in self.__dict__.items() if key != '_Task__log'}
        self.log_info(f'{config}')
        if getattr(kwargs, 'dryrun', False):
            print(render_string(str(config), **kwargs))
        return config
