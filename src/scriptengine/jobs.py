""" ScriptEngine jobs.

Jobs are the second level (above tasks) work unit in ScriptEngine. Jobs are
made of tasks and may include loops, conditionals, and a context. Job lists can
be given to a ScriptEngine, for execution.
"""

import ast
import copy
import logging
import uuid

from scriptengine.context import Context
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
        except ScriptEngineParseJinjaError as e:
            self.log_error(
                f"Jinja2 error in *when* clause '{self._when}' (full error: {e})"
            )
            raise ScriptEngineJobParseError

    def loop_spec(self, context):
        try:
            iter = j2render(self._loop, context)
        except ScriptEngineParseJinjaError as e:
            self.log_error(
                f"Jinja2 error in *loop* spec '{self._loop}' (full error: {e})"
            )
            raise ScriptEngineJobParseError
        if isinstance(iter, str):
            try:
                iter = ast.literal_eval(iter or "None")
            except (SyntaxError, ValueError) as e:
                self.log_error(
                    f"AST evaluation error in *loop* spec '{iter}' (full error: {e})"
                )
                raise ScriptEngineJobParseError
        if isinstance(iter, dict):
            iter = iter.items()
            vars = self._loop_vars or ("key", "value")
        else:
            vars = self._loop_vars or ("item",)
        return iter, vars

    def loop(self, context):
        if self._loop:
            iter, vars = self.loop_spec(context)
            if iter:
                for items in iter:
                    parsed_items = tuple(
                        j2render(i, context) for i in _listy(items, type_=tuple)
                    )
                    vars_tuple = _listy(vars, type_=tuple)
                    if len(vars_tuple) == 1 and len(parsed_items) > 1:
                        # If only one loop variable is given and items is listy,
                        # assign the whole list to the variable (see #59)
                        yield {vars_tuple[0]: parsed_items}
                    else:
                        # Otherwise, map (zip) loop vars with items
                        # Note that extra vars or items are ignored!
                        yield dict(zip(vars_tuple, parsed_items))
            else:
                self.log_warning(
                    "Null loop after parsing loop descriptor, job is not run!"
                )
                raise StopIteration
        else:
            yield {}

    def append(self, todo):
        todo_list = _todo_list(todo)
        self._todo.extend(todo_list)
        self.log_debug(f'Append: {",".join(t.shortid for t in todo_list)}')

    def run(self, context):
        if self.when(context):
            local_context = Context(copy.deepcopy(context))
            context_update = Context()
            for items in self.loop(local_context):
                if set(items) & set(local_context):
                    self.log_warning(
                        "The following loop variables collide with the "
                        f"context: {set(items) & set(local_context)}"
                    )
                for t in self.todo:
                    c = t.run(Context({**local_context, **items}))
                    if c:
                        local_context += c
                        context_update += c
            return context_update or None

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
