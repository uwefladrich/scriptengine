""" ScriptEngine jobs.

Jobs are the second level (above tasks) work unit in ScriptEngine. Jobs are
made of tasks and may include loops, conditionals, and a context. Job lists can
be given to a ScriptEngine, for execution.
"""

import logging
import uuid
import ast

from se.helpers import render_string

class Job:

    def __init__(self, when=None, loop=None):
        self._identifier = uuid.uuid4()
        self._todo = []
        self._when = when
        self._loop = loop

        self._logger = logging.getLogger(__name__)
        self.log_debug(f"Create Job"
                       f"{', when='+self._when if self._when else ''}"
                       f"{', loop='+str(self._loop) if self._loop else ''}")

    @property
    def id(self):
        return self._identifier

    @property
    def todo(self):
        return iter(self._todo)

    def when(self, context):
        return self._when is None or render_string(self._when, context, boolean=True)

    def loop(self, context):
        try:
            rendered_loop_string = render_string(self._loop, context)
        except TypeError:
            return None
        else:
            return ast.literal_eval(rendered_loop_string)

    def append(self, todo):
        todo_as_list = todo if isinstance(todo, list) else [todo]
        self.log_debug(f"Append: {','.join([str(t.id) for t in todo_as_list])} to")
        self._todo.extend(todo_as_list)

    def log_debug(self, message):
        self._logger.debug(f"{message} ({self.id})")

    def log_info(self, message):
        self._logger.info(f"{message} ({self.id})")

    def log_warning(self, message):
        self._logger.warning(f"{message} ({self.id})")

    def log_error(self, message):
        self._logger.error(f"{message} ({self.id})")
