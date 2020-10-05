"""Chdir task for ScriptEngine."""

import os

from scriptengine.tasks.base import Task
from scriptengine.tasks.base.timing import timed_runner


class Chdir(Task):
    """Chdir task, changes the current working directory
    """
    def __init__(self, parameters):
        super().__init__(parameters, required_parameters=["path"])

    @timed_runner
    def run(self, context):
        path = self.getarg('path', context)
        self.log_info(f"Change path to {path}")
        os.chdir(path)
