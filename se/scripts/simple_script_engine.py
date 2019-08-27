""" SimpleScriptEngine for ScriptEngine.

SimpleScriptEngine is a simplistic script engine. It runs all jobs sequentially
on the local machine, without consideration of job contexts.
"""

from deepmerge import always_merger

class SimpleScriptEngine:
    """Simplistic script engine for ScriptEngine.
    """
    def run(self, job_or_task, context):
        try:
            job_or_task.run(context)
        except AttributeError:
            if job_or_task.when(context):
                none_loop = object()
                for item in job_or_task.loop(context) or [none_loop]:
                    if item is not none_loop:
                        context["item"] = item
                    for todo in job_or_task.todo:
                        try:
                            todo.run(context)
                        except AttributeError:
                            self.run(todo, context)
