"""Exit task for ScriptEngine."""

import sys

from se.tasks import Task


class Exit(Task):
    """Exit task, stops by calling sys.exit
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["msg"])

    def __str__(self):
        return f"Exit: {self.msg}"

    def run(self, context):
        self.log_info(self.msg)
        sys.exit()
