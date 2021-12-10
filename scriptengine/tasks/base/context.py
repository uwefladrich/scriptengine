"""Context task for ScriptEngine."""

from scriptengine.context import ContextUpdate
from scriptengine.tasks.core import Task, timed_runner


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
