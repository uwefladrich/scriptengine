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
        path = os.path.normpath(j2render(self.path, context))
        path_depth = path.count(os.path.sep)

        pattern = j2render(getattr(self, "pattern", "*"), context)

        find_type = j2render(getattr(self, "type", "file"), context)
        if find_type not in ("file", "dir"):
            self.log_error(f"Invalid 'type': {find_type} "
                           "(must be either 'file' or 'dir')")
            raise ScriptEngineStopException(f"Invalid 'type' argument in find task")

        max_depth = j2render(getattr(self, "depth", "-1"), context)
        try:
            max_depth = max(-1, int(max_depth))
        except (ValueError, TypeError):
            self.log_error(f"Invalid 'depth': {max_depth} (must be an integer)")
            raise ScriptEngineStopException(f"Invalid 'depth' argument in find task")

        self.log_info(f"Find {find_type} with pattern '{pattern}' "
                      f"in {path} (with max depth={max_depth})")
        result = []
        for root, dirs, files in os.walk(path):
            if find_type == "file":
                files_or_dirs = files
            else:
                files_or_dirs = dirs
            for name in files_or_dirs:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.normpath(os.path.join(root, name)))
            if max_depth >= 0 and root.count(os.path.sep) >= path_depth+max_depth:
                del dirs[:]
        if result:
            self.log_debug(f"Found: {result}")
        else:
            self.log_debug(f"Nothing found")
        result_key = getattr(self, "set_context", "result")
        self.log_debug(f"Store result under context key '{result_key}'")
        context[result_key] = result
