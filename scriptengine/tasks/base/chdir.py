"""Chdir task for ScriptEngine."""

import os

from scriptengine.tasks.base import Task


class Chdir(Task):
    """Chdir task, changes the current working directory
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["path"])

    def run(self, context):
        path = self.getarg('path', context)
        self.log_info(f"Change path to {path}")
        os.chdir(path)
