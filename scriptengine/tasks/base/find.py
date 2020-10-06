"""Find task for ScriptEngine"""

import os
import fnmatch

from scriptengine.tasks.base import Task
from scriptengine.tasks.base.timing import timed_runner
from scriptengine.exceptions import ScriptEngineStopException


class Find(Task):
    """Find task, finds files or directories by name patterns
    """
    _required_arguments = ('path', )

    def __init__(self, arguments):
        Find.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        path = os.path.normpath(self.getarg('path', context))
        path_depth = path.count(os.path.sep)

        pattern = self.getarg('pattern', context, default='*')

        find_type = self.getarg('type', context, default='file')
        if find_type not in ("file", "dir"):
            self.log_error(f"Invalid 'type': {find_type} "
                           "(must be either 'file' or 'dir')")
            raise ScriptEngineStopException("Invalid 'type' argument in find task")

        max_depth = self.getarg('depth', context, default=-1)
        try:
            max_depth = max(-1, int(max_depth))
        except (ValueError, TypeError):
            self.log_error(f"Invalid 'depth': {max_depth} (must be an integer)")
            raise ScriptEngineStopException("Invalid 'depth' argument in find task")

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
            self.log_debug("Nothing found")
        result_key = self.getarg('set', context, default='result')
        self.log_debug(f"Store result under context key '{result_key}'")
        context[result_key] = result
