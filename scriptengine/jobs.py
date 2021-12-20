""" ScriptEngine jobs.

Jobs are the second level (above tasks) work unit in ScriptEngine. Jobs are
made of tasks and may include loops, conditionals, and a context. Job lists can
be given to a ScriptEngine, for execution.
"""

import ast
import logging
import uuid

from scriptengine.context import Context, ContextUpdate, save_copy
from scriptengine.exceptions import (
    ScriptEngineJobParseError,
    ScriptEngineParseJinjaError,
)
from scriptengine.jinja import render as j2render
from scriptengine.tasks.core import Task


def _listy(thing, type_=list):
    if isinstance(thing, str) or isinstance(thing, dict):
        return type_((thing,))
    try:
        iter(thing)
    except TypeError:
        return type_((thing,))
    else:
        return type_(thing)


def _is_todo(thing):
    return isinstance(thing, Task) or isinstance(thing, Job)


def _todo_list(todo):
    todo_list = _listy(todo)
    if not all(_is_todo(t) for t in todo_list):
        raise ValueError("A todo list must be made of Tasks and/or Jobs")
    return todo_list


class Job:
    def __init__(self, todo=None, *, when=None, loop=None, loop_vars=None):
        self._identifier = uuid.uuid4()
        self.todo = todo or []
        self._when = when
        self._loop = loop
        self._loop_vars = loop_vars
        self.log_debug(
            "New Job:"
            f"{' when '+self._when if self._when else ''}"
            f"{' with '+str(self._loop_vars) if self._loop else ''}"
            f"{' in '+str(self._loop) if self._loop else ''}"
            f" {tuple(t.shortid for t in self._todo)}"
        )

    @property
    def id(self):
        return self._identifier

    @property
    def shortid(self):
        return self._identifier.hex[:10]

    @property
    def todo(self):
        return self._todo

    @todo.setter
    def todo(self, todo):
        self._todo = _todo_list(todo)

    def when(self, context):
        try:
            return self._when is None or j2render(self._when, context, boolean=True)
        except ScriptEngineParseJinjaError:
            self.log_error(
                "Error while parsing (Jinja2) invalid when clause "
                f'"{self._when}" with context "{context}"'
            )
            raise ScriptEngineJobParseError

    def loop(self, context):
        if self._loop:
            try:
                loop_iter = j2render(self._loop, context)
            except ScriptEngineParseJinjaError:
                self.log_error(
                    "Error while parsing (Jinja2) invalid loop expression "
                    f'"{self._loop}" with context "{context}"'
                )
                raise ScriptEngineJobParseError
            if isinstance(loop_iter, str):
                try:
                    loop_iter = ast.literal_eval(loop_iter or "None")
                except (SyntaxError, ValueError):
                    self.log_error(
                        "Error while evaluating (AST) invalid loop expression "
                        f'"{loop_iter}" with context "{context}"'
                    )
                    raise ScriptEngineJobParseError
            if isinstance(loop_iter, dict):
                loop_iter = loop_iter.items()
                loop_vars = self._loop_vars or ("key", "value")
            else:
                loop_vars = self._loop_vars or ("item",)
            if loop_iter:
                for items in loop_iter:
                    yield dict(
                        zip(
                            _listy(loop_vars, type_=tuple),
                            (j2render(i, context) for i in _listy(items, type_=tuple)),
                        )
                    )
            else:
                self.log_warning(
                    "Loop descriptor evaluates to false after parsing, job is not run!"
                )
        else:
            yield {}

    def append(self, todo):
        todo_list = _todo_list(todo)
        self._todo.extend(todo_list)
        self.log_debug(f'Append: {",".join(t.shortid for t in todo_list)}')

    def run(self, context):
        if self.when(context):
            local_context = Context(save_copy(context))
            for items in self.loop(local_context):
                if set(items) & set(local_context):
                    self.log_warning(
                        "The following loop variables collide with the "
                        f"context: {set(items) & set(local_context)}"
                    )
                for t in self.todo:
                    context_update = t.run(Context({**local_context, **items}))
                    if context_update:
                        local_context += context_update
            return ContextUpdate(context, local_context)

    def _log(self, level, msg):
        logging.getLogger("se.job").log(level, msg, extra={"id": self.shortid})

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
