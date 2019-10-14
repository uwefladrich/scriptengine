"""Copy task for ScriptEngine."""

import shutil

from se.tasks import Task
from se.helpers import render_string


class Copy(Task):
    """Copy task, copies a file.

    The task needs a source and a destination and copies a file with the shutil
    module.

    Args:
        dictionary (dict): Must at least contain the following keys:
            - src: Source file name
            - dst: Destination file or directory name
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["src", "dst"])

    def __str__(self):
        return f"Copy: {self.src} --> {self.dst}"

    def run(self, context):
        self.log_info(f"{self.src} --> {self.dst}")
        shutil.copy(render_string(self.src, context), render_string(self.dst, context))
