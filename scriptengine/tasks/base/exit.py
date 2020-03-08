"""Exit task for ScriptEngine."""

import sys

from scriptengine.tasks import Task
from scriptengine.exceptions import ScriptEngineStopException


class Exit(Task):
    """Exit task, stops by calling sys.exit
    """
    def __init__(self, parameters=None):
        super().__init__(__name__, parameters)

    def __str__(self):
        return f"Exit {getattr(self, 'msg', '')}"

    def run(self, context):
        self.log_info(getattr(self, "msg", "Requesting ScriptEngine to stop"))
        raise ScriptEngineStopException("Exit task requests stopping ScriptEngine")
