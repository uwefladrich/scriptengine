"""Chdir task for ScriptEngine."""

import os

from scriptengine.tasks import Task
from scriptengine.jinja import render as j2render


class Chdir(Task):
    """Chdir task, changes the current working directory
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["path"])

    def __str__(self):
        return f"Chdir: {self.path}"

    def run(self, context):
        path = j2render(self.path, context)
        self.log_info(f"Change path to {path}")
        os.chdir(path)
