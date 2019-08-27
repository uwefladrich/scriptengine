"""Echo task for ScriptEngine."""

from se.tasks import Task
from se.helpers import render_string

from se.helpers import terminal_colors as tc


class Echo(Task):
    """Echo task, writes a (coloured) message to stdout
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["msg"])

    def __str__(self):
        return f"Echo: {self.msg}"

    def run(self, context):
        self.log_info(f"{render_string(self.msg, context)}")
        print(f"{tc.LIGHTBLUE}{render_string(self.msg, context)}{tc.RESET}")
