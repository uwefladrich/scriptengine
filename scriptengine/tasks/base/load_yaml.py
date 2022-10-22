import os
from pathlib import Path
import yaml

from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.tasks.core import Task, timed_runner
from scriptengine.context import ContextUpdate


class LoadYaml(Task):

    _required_arguments = ("src",)

    def __init__(self, arguments):
        LoadYaml.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        self.log_info("Execute load_yaml command")

        src = self.getarg("src", context)
        section = self.getarg("section", context, default=None)
        self.log_debug(f"Load the yaml file {src} into the context")

        try:
            with open(src, "r") as f:
                file_dict = yaml.load(f, Loader=yaml.SafeLoader)
        except FileNotFoundError:
            self.log_error(f"Yaml file not found: {src}")
            raise ScriptEngineTaskRunError

        if section:
            esm_dict = {section: file_dict}
        else:
            esm_dict = file_dict

        context_update = ContextUpdate(
            esm_dict
        )
        self.log_info(f"Context update: with info from {src}")
        return context_update
