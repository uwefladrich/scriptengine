"""Exit task for ScriptEngine."""

from scriptengine.tasks.base import Task
from scriptengine.exceptions import ScriptEngineStopException


class Exit(Task):
    """Exit task, run method throws ScriptEngineStopException
    """
    def run(self, context):
        msg = self.getarg('msg', context,
                          default='Requesting ScriptEngine to stop')
        self.log_info(msg)
        raise ScriptEngineStopException(
                        'Exit task requests stopping ScriptEngine')
