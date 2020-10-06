"""Context task for ScriptEngine."""

import yaml
from deepmerge import always_merger

import scriptengine.jinja
from scriptengine.tasks.base import Task
from scriptengine.tasks.base.timing import timed_runner


class Context(Task):
    """Context task, sets parameters in the SE context

       The tasks run() method processes, recursively, a dictionary of key:value
       pairs and adds them to the context. The parameter values are rendered
       with Jinja2 and YAML unless they are of the special NoParse*String
       string types (see the YAML constructors defined in yaml.py).
    """

    @timed_runner
    def run(self, context):

        def evaluate_params(parameters, context):
            """Recursively evaluates parameter dict by parsing with Jinja2 and
               reparsing with YAML
            """
            evaluated_params = {}
            for key, val in parameters.items():

                if isinstance(val, str):
                    if not isinstance(val,
                                      scriptengine.yaml.NoParseJinjaString):
                        # Make sure that a NoParseString is still a
                        # NoParseString after this!
                        val = type(val)(scriptengine.jinja.render(val,
                                                                  context))

                    if not isinstance(val,
                                      scriptengine.yaml.NoParseYamlString):
                        # Try to reload the item through YAML, in order to
                        # get the right type
                        # Otherwise, everything would be just a string
                        try:
                            val = yaml.full_load(val)
                        # However, it may really be a string that is
                        # no valid YAML!
                        except (yaml.parser.ParserError,
                                yaml.constructor.ConstructorError):
                            self.log_debug(f'Reparsing argument "{val}" '
                                           'with YAML failed')

                    # For consistency, we always return plain strings
                    if isinstance(val, scriptengine.yaml.NoParseString):
                        val = str(val)

                    evaluated_params[key] = val

                elif isinstance(val, dict):
                    evaluated_params[key] = evaluate_params(val, context)

                else:
                    evaluated_params[key] = val

            return evaluated_params

        params = {key: val for key, val in self.__dict__.items()
                  if not (isinstance(key, str) and key.startswith('_'))}
        self.log_info(f'{", ".join([f"{k}={params[k]}" for k in params])}')

        add_to_context = evaluate_params(params, context)
        self.log_debug(f'Adding to context: {add_to_context}')
        always_merger.merge(context, add_to_context)
