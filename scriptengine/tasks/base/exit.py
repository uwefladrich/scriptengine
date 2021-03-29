"""Exit task for ScriptEngine."""

from scriptengine.tasks.core import Task
from scriptengine.exceptions import ScriptEngineStopException


class Exit(Task):
    """Exit task, run method throws ScriptEngineStopException
    """
    def run(self, context):
        self.log_info(
            self.getarg(
                'msg',
                context,
                default='Requesting ScriptEngine to STOP'
            )
        )
        raise ScriptEngineStopException
