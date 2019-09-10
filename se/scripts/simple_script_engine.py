""" SimpleScriptEngine for ScriptEngine.

SimpleScriptEngine is a simplistic script engine. It runs all jobs sequentially
on the local machine, without consideration of job contexts.
"""

class SimpleScriptEngine:
    """Simplistic script engine for ScriptEngine.
    """
    def run(self, script, context):
        for script_item in script if isinstance(script, list) else [script]:
            try:
                # Assume script_item is a task (i.e. has a run() method)
                script_item.run(context)
            except AttributeError: # script_item is a job, not a task
                if script_item.when(context):
                    none_loop = object() # just make sure none_loop is unique
                    for loop_item in script_item.loop(context) or [none_loop]:
                        if loop_item is not none_loop:
                            context["item"] = loop_item
                        for todo in script_item.todo:
                            try:
                                # Same as above, assume task ...
                                todo.run(context)
                            except AttributeError:
                                # ... otherwise, recurse for job
                                self.run(todo, context)
