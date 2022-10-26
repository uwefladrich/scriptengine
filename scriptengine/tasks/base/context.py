"""Context task for ScriptEngine."""

from scriptengine.context import ContextUpdate
from scriptengine.tasks.core import Task, timed_runner
from scriptengine.exceptions import ScriptEngineTaskError


class Context(Task):
    """Context task, sets/updates the SE context.
    The context task takes name, value pairs as arguments and updates the SE
    context accordingly. Values can be scalars, lists, dictionaries and nested
    combinations thereof.
    Note that Context.run() returns a context *update* and that the higher-level
    running instance (a Job or a ScriptEngine instance) is responsible for
    merging the update with an existing context dict."""

    @timed_runner
    def run(self, context):
        context_update = ContextUpdate(
            {n: self.getarg(n, context) for n in vars(self) if not n.startswith("_")}
        )
        self.log_info(f"Context update: {context_update}")
        return context_update


class ContextFrom(Task):
    """
    This task updates the context, just as the Context task, but from sources
    other than direct arguments.

    If the 'dict' argument is given, the argument value must be a dict and is
    used to update the context, e.g.

    - base.context:
        upd:
            foo: 1
    - base.context.from:
        dict: "{{upd}}"

    If the 'file' argument is given, the argument value must be a file name and
    the context is updated from the file context. The file format must be YAML:

    - base.context.from:
        file: update.yml
    """

    @timed_runner
    def run(self, context):
        ctx_dict = self.getarg("dict", context, default=False)
        ctx_file = self.getarg("file", context, default=False)
        if ctx_dict and ctx_file:
            self.log_error("Task arguments 'dict' and 'file' are mutual exclusive")
            raise ScriptEngineTaskError
        if ctx_dict:
            self.log_info(f"Context update from dict: {ctx_dict}")
            return ContextUpdate(ctx_dict)
        elif ctx_file:
            ...
        else:
            self.log_error("Missing argument: either 'dict' or 'file' is needed")
            raise ScriptEngineTaskError
