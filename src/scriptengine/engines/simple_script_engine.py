""" SimpleScriptEngine for ScriptEngine.

SimpleScriptEngine is a simplistic script engine. It runs all jobs sequentially
on the local machine, without consideration of job contexts. The
SimpleScriptEngine relies on the Job class to run the actual tasks/jobs.
"""

import logging
import sys
from pprint import pprint

from scriptengine.context import Context, ContextUpdate, save_copy
from scriptengine.exceptions import (
    ScriptEngineJobError,
    ScriptEngineStopException,
    ScriptEngineTaskError,
)
from scriptengine.tasks.core import Task


class SimpleScriptEngine:
    def __init__(self):
        self.logger = logging.getLogger(
            "se.instance." + self.__class__.__name__.lower()
        )

    def _guarded_run(self, runner, context):
        try:
            return runner.run(context)
        except AttributeError as e:
            self.log_error(
                "STOPPING SimpleScriptEngine due to internal error: "
                f"Cannot run type {type(runner).__name__}"
            )
            error = e
        except ScriptEngineStopException:
            self.log_info("STOPPING SimpleScriptEngine instance upon request")
            error = None
        except ScriptEngineTaskError as e:
            if isinstance(runner, Task):
                self.log_error(
                    "STOPPING SimpleScriptEngine due to task error in "
                    f"{runner.reg_name} <{runner.shortid}>"
                )
            else:
                self.log_error(
                    "STOPPING SimpleScriptEngine due to task error in job "
                    f"<{runner.shortid}>"
                )
            error = e
        except ScriptEngineJobError as e:
            self.log_error(
                f"STOPPING SimpleScriptEngine due to job error in <{runner.shortid}>"
            )
            error = e
        if error:
            if self.logger.getEffectiveLevel() <= logging.DEBUG:
                self.log_error("Last context before error:")
                pprint(context)
                self.log_error("Traceback from error:")
                raise error
            else:
                self.log_error("For more debugging info, re-run with loglevel DEBUG")
        sys.exit()

    def run(self, script, context):
        local_context = Context(save_copy(context))
        for todo in script if isinstance(script, list) else [script]:
            context_update = self._guarded_run(todo, local_context)
            if context_update:
                local_context += context_update
        return ContextUpdate(context, local_context)

    def _log(self, level, msg):
        self.logger.log(level, msg)

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
