"""Exit task for ScriptEngine."""

from scriptengine.tasks.base import Task
from scriptengine.exceptions import ScriptEngineStopException


class Exit(Task):
    """Exit task, stops by calling sys.exit
    """
    def __init__(self, parameters=None):
        super().__init__(__name__, parameters)

    def run(self, context):
        msg = self.getarg('msg', context, default='Requesting ScriptEngine to stop')
        self.log_info(msg)
        raise ScriptEngineStopException("Exit task requests stopping ScriptEngine")
