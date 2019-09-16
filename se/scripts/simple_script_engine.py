""" SimpleScriptEngine for ScriptEngine.

SimpleScriptEngine is a simplistic script engine. It runs all jobs sequentially
on the local machine, without consideration of job contexts.
"""

import sys
import logging

from se.tasks import Task
from se.jobs import Job
from se.scripts.logging import app_logger
from se.exceptions import ScriptEngineStopException

class SimpleScriptEngine:
    """Simplistic script engine for ScriptEngine.
    """

    def __init__(self, log_level=logging.INFO):
        self._logger = app_logger(self.__class__.__name__, level=log_level)

    def _guarded_run(self, item, context):
        try:
            item.run(context)
        except ScriptEngineStopException as e:
            self._logger.info(e)
            sys.exit()

    def run(self, script, context):
        for script_item in script if isinstance(script, list) else [script]:
            if isinstance(script_item, Task):
                self._guarded_run(script_item, context)
            elif isinstance(script_item, Job):
                if script_item.when(context):
                    none_loop = object() # just create a unique object
                    for loop_item in script_item.loop(context) or [none_loop]:
                        if loop_item is not none_loop:
                            context["item"] = loop_item
                        for todo in script_item.todo:
                            if isinstance(todo, Task):
                                self._guarded_run(todo, context)
                            elif isinstance(todo, Job):
                                # recurse for jobs
                                self.run(todo, context)
                            else:
                                raise RuntimeError(f"Can only run Tasks or Jobs, "
                                                   f"found: {type(script_item)}")
            else:
                raise RuntimeError(f"Can only run Tasks or Jobs, found: {type(script_item)}")
