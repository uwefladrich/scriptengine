"""Echo task for ScriptEngine."""

from se.tasks import Task
from se.helpers import render_string

from se.helpers import terminal_colors as tc


class Echo(Task):
    """Echo task, writes a message to stdout
    """
    def __init__(self, dictionary):
        super().__init__(__name__, dictionary, 'msg')

    def __str__(self):
        return f'Echo: {self.msg}'

    def run(self, **kwargs):
        self.log_info(f'{render_string(self.msg, **kwargs)}')
        if getattr(kwargs, 'dryrun', False):
            print(render_string(str(self), **kwargs))
        else:
            print(f'{tc.LIGHTBLUE}{render_string(self.msg, **kwargs)}{tc.RESET}')
