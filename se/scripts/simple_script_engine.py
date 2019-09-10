""" SimpleScriptEngine for ScriptEngine.

SimpleScriptEngine is a simplistic script engine. It runs all jobs sequentially
on the local machine, without consideration of job contexts.
"""

import sys
import logging

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
            try:
                # Assume script_item is a task (i.e. has a run() method)
                self._guarded_run(script_item, context)
            except AttributeError: # script_item is a job, not a task
                if script_item.when(context):
                    none_loop = object() # just make sure none_loop is unique
                    for loop_item in script_item.loop(context) or [none_loop]:
                        if loop_item is not none_loop:
                            context["item"] = loop_item
                        for todo in script_item.todo:
                            try:
                                # Same as above, assume task ...
                                self._guarded_run(todo, context)
                            except AttributeError:
                                # ... otherwise, recurse for job
                                self.run(todo, context)
