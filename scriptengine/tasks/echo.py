"""Echo task for ScriptEngine."""

from scriptengine.tasks import Task
from scriptengine.helpers import render_string

from scriptengine.helpers import terminal_colors as tc


class Echo(Task):
    """Echo task, writes a (coloured) message to stdout
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["msg"])

    def __str__(self):
        return f"Echo: {self.msg}"

    def run(self, context):
        self.log_info(self.msg)
        print(f"{tc.LIGHTBLUE}{render_string(self.msg, context)}{tc.RESET}")