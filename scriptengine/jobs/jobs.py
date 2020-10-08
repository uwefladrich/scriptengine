""" ScriptEngine jobs.

Jobs are the second level (above tasks) work unit in ScriptEngine. Jobs are
made of tasks and may include loops, conditionals, and a context. Job lists can
be given to a ScriptEngine, for execution.
"""

import logging
import uuid
import ast

from scriptengine.jinja import render as j2render
from scriptengine.exceptions import ScriptEngineParseError


class Job:

    def __init__(self, when=None, loop=None):
        self._identifier = uuid.uuid4()
        self._todo = []
        self._when = when

        if loop is None:
            self._loop_var = None
            self._loop_iter = None
        elif isinstance(loop, dict):
            self._loop_var = loop.get("with", "item")
            self._loop_iter = loop.get("in", None)
        else:  # loop is assumed list
            self._loop_var = "item"
            self._loop_iter = loop

        self.log_debug(
                f'Create Job'
                f'{" when "+self._when if self._when else ""}'
                f'{" with "+str(self._loop_var) if self._loop_var else ""}'
                f'{" in "+str(self._loop_iter) if self._loop_iter else ""}')

    @property
    def id(self):
        return self._identifier

    @property
    def shortid(self):
        return self._identifier.hex[:10]

    @property
    def todo(self):
        return iter(self._todo)

    def when(self, context):
        return (self._when is None
                or j2render(self._when, context, boolean=True))

    def loop(self, context):
        loop_iter = j2render(self._loop_iter, context)
        if isinstance(loop_iter, str):
            try:
                loop_iter = ast.literal_eval(loop_iter)
            except SyntaxError:
                raise ScriptEngineParseError(
                        'Syntax error while evaluating loop expression '
                        f'"{loop_iter}" in job with id {self.id}')
        return self._loop_var, loop_iter

    def append(self, todo):
        todo_as_list = todo if isinstance(todo, list) else [todo]
        self.log_debug(
                f"Append: {','.join([str(t.id) for t in todo_as_list])} to")
        self._todo.extend(todo_as_list)

    def _log(self, level, msg):
        logging.getLogger('se.job').log(level, msg, extra={'id': self.shortid})

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
