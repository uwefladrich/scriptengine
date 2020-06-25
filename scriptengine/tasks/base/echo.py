"""Echo task for ScriptEngine."""

from scriptengine.tasks.base import Task
from scriptengine.tasks.base.timing import timed_runner

from scriptengine.helpers import terminal_colors as tc


class Echo(Task):
    """Echo task, writes a (coloured) message to stdout
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=['msg'])

    def __str__(self):
        return f'Echo: {self.msg}'

    @timed_runner
    def run(self, context):
        self.log_info(self.msg)
        msg = self.getarg('msg', context)
        print(tc.LIGHTBLUE + str(msg) + tc.RESET)
