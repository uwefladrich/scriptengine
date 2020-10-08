""" SimpleScriptEngine for ScriptEngine.

SimpleScriptEngine is a simplistic script engine. It runs all jobs sequentially
on the local machine, without consideration of job contexts.
"""

import sys
import logging

from scriptengine.tasks.base import Task
from scriptengine.jobs import Job
from scriptengine.exceptions import ScriptEngineError, \
                                    ScriptEngineStopException


class SimpleScriptEngine:
    """Simplistic script engine for ScriptEngine.
    """

    def _guarded_run(self, item, context):
        try:
            item.run(context)
        except ScriptEngineStopException as e:
            self.log_info(e)
            sys.exit()

    def run(self, script, context):

        for script_item in script if isinstance(script, list) else [script]:

            if isinstance(script_item, Task):
                self._guarded_run(script_item, context)
            elif isinstance(script_item, Job):
                if script_item.when(context):

                    # Loop setup with loop var collision detection
                    none_loop = object()  # just a unique object
                    loop_var, loop_iter = script_item.loop(context)
                    old_loop_var = context.get(loop_var, None)
                    if old_loop_var:
                        self.log_warning("Loop variable collision "
                                         f"for '{loop_var}'")

                    # Run loop (at least once)
                    for loop_item in loop_iter or [none_loop]:

                        if loop_item is not none_loop:
                            context[loop_var] = loop_item

                        # Run task/job for one loop iteration
                        for todo in script_item.todo:
                            if isinstance(todo, Task):
                                self._guarded_run(todo, context)
                            elif isinstance(todo, Job):
                                # recurse for jobs
                                self.run(todo, context)
                            else:
                                raise ScriptEngineError(
                                            "Invalid item "
                                            "(neither Task nor Job) "
                                            f"of type {type(script_item)}")
                    # Remove or restore loop var
                    if old_loop_var:
                        context[loop_var] = old_loop_var
                    else:
                        context.pop(loop_var, None)
                else:
                    self.log_debug(
                        f'Not executing <{script_item.shortid}> because '
                        'when clause evaluates false')
            else:
                raise ScriptEngineError("Invalid item (neither Task nor Job) "
                                        f"of type {type(script_item)}")

    def _log(self, level, msg):
        logger = 'se.instance.'+self.__class__.__name__.lower()
        logging.getLogger(logger).log(level, msg)

    def log_debug(self, msg):
        self._log(logging.DEBUG, msg)

    def log_info(self, msg):
        self._log(logging.INFO, msg)

    def log_warning(self, msg):
        self._log(logging.WARNING, msg)

    def log_error(self, msg):
        self._log(logging.ERROR, msg)

    def log_critical(self, msg):
        self._log(logging.CRITICAL, msg)
