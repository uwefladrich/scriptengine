"""Config task for ScriptEngine."""

from deepmerge import always_merger

from scriptengine.tasks import Task
from scriptengine.jinja import render as j2render


class Config(Task):
    """Config task, sets configuration parameters.

    The tasks run() method returns all name-value pairs passed at creation time
    in a dict.
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters)

    def __str__(self):
        return f"Config: {self.__dict__}"

    def run(self, context):
        parameters = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                if isinstance(value, str) and value.startswith("_eval_"):
                    value = j2render(value[6:], context)
                parameters[key] = value
        self.log_info(f"{parameters}")
        always_merger.merge(context, parameters)
