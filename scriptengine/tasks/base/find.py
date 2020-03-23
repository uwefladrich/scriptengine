"""Find task for ScriptEngine"""

import os
import fnmatch

from scriptengine.tasks import Task
from scriptengine.jinja import render as j2render
from scriptengine.exceptions import ScriptEngineStopException

class Find(Task):
    """Find task, finds files or directories by name patterns
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["path"])

    def run(self, context):
        path = j2render(self.path, context)
        pattern = j2render(getattr(self, "pattern", "*"), context)
        find_type = j2render(getattr(self, "type", "file"), context)

        if find_type not in ("file", "dir"):
            self.log_error(f"Invalid type: {find_type} "
                           "(must be either 'file' or 'dir')")
            raise ScriptEngineStopException(f"Invalid 'type' argument in find task")

        self.log_info(f"Find {find_type} with pattern '{pattern}' "
                      f"in {path}")
        result = []
        for root, dirs, files in os.walk(path):
            if find_type == "file":
                files_or_dirs = files
            else:
                files_or_dirs = dirs
            for name in files_or_dirs:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        if result:
            self.log_debug(f"Found: {result}")
        else:
            self.log_debug(f"Nothing found")
        result_key = getattr(self, "set_context", "result")
        self.log_debug(f"Store result under context key '{result_key}'")
        context[result_key] = result
