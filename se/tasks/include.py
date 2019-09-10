"""Include task for ScriptEngine

   The Include task reads a YAML file, parses the content to create a
   ScriptEngine script and lets the active ScriptEngine instance execute it.
"""

import se.scripts
from se.tasks import Task
from se.helpers import render_string

class Include(Task):

    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["src"])

    def __str__(self):
        return f"Include: {self.src}"

    def run(self, context):
        self.log_info(self.src)
        self.log_debug(f"Parsing script from '{render_string(self.src, context)}'")
        script = se.scripts.parse_yaml_file(render_string(self.src, context))
        try:
            se_instance = context['_se_instance']
        except KeyError:
            raise RuntimeError(f"ScriptEngine instance not found")
        else:
            self.log_debug(f"Executing todos from '{render_string(self.src, context)}'")
            se_instance.run(script, context)
            self.log_debug(f"Finished executing todos from '{render_string(self.src, context)}'")
