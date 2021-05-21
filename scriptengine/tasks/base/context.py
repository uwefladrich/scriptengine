"""Context task for ScriptEngine."""

from deepmerge import always_merger

from scriptengine.tasks.core import Task, timed_runner


class Context(Task):
    """Context task, sets/updates parameters in the SE context
    Context.run() creates a dictionary from all name, value pairs of its
    arguments and updates the context with that dict. The update algorithm used
    here is deepmerge.always_merger, which means that all non-conflicting
    updates are merged and in the case of conflicts, the data from the task
    arguments overwrite the context.
    """
    @timed_runner
    def run(self, context):
        context_update = {
            n: self.getarg(n, context)
            for n in vars(self) if not n.startswith('_')
        }
        self.log_info(f'Adding to context: {context_update}')
        always_merger.merge(context, context_update)
