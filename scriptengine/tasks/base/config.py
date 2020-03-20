"""Config task for ScriptEngine."""

import yaml
from deepmerge import always_merger

from scriptengine.tasks import Task
from scriptengine.jinja import render as j2render


class Config(Task):
    """Config task, sets configuration parameters.

    The tasks run() method processes, recursively, a dictionary of
    name:parameter pairs and adds them to the context. The parameter values are
    rednered with Jinja2 (j2render function) unless they are strings starting
    with "_noeval_" (see the YAML !noeval constructor in yaml.py).
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters)

    def __str__(self):
        return f"Config: {self.__dict__}"

    def run(self, context):

        def eval_dict(arg_dict, context):
            evaluated_dict = {}
            for key, param in arg_dict.items():
                if not isinstance(key, str):
                    self.log_error(f"Config keys must be strings! "
                                   f"Invalid non-string key: \"{key}\"")
                    raise RuntimeError(f"Invalid non-string key: \"{key}\"")
                if not key.startswith("_"):
                    if isinstance(param, str):
                        rendered_param = j2render(param, context)
                        # Try to reload the item through YAML, in order to
                        # get the right type
                        # Otherwise, everything would be just a string
                        try:
                            evaluated_dict[key] = yaml.full_load(rendered_param)
                        # However, it may really be a string that is no valid YAML!
                        except (yaml.parser.ParserError, yaml.constructor.ConstructorError):
                            evaluated_dict[key] = rendered_param
                    elif isinstance(param, dict):
                        evaluated_dict[key] = eval_dict(param, context)
                    else:
                        evaluated_dict[key] = param
            return evaluated_dict

        config_params = eval_dict(self.__dict__, context)
        self.log_info(f"Config params: {config_params}")
        always_merger.merge(context, config_params)
