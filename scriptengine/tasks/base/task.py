"""ScriptEngine task module.

Provides the base class for all tasks.
"""

import logging
import uuid
import yaml

import scriptengine.jinja
import scriptengine.yaml


_SENTINEL = object()


class Task:

    def __init__(self, logger_name, parameters=None, required_parameters=None):

        self._identifier = uuid.uuid4()

        if 'run' in (parameters or []):
            raise RuntimeError('Reserved identifier "run" used as parameter while creating task')
        self.__dict__.update(parameters or {})

        for param in (required_parameters or []):
            if param not in self.__dict__:
                raise RuntimeError(f"Missing required parameter '{param}' while creating "
                                   f"'{type(self).__name__}' task from {parameters!s}")
        self._logger = logging.getLogger(logger_name)
        self.log_debug(f'Created task: {repr(self)}')

    @property
    def id(self):
        return self._identifier

    def __repr__(self):
        params = {key:val for key, val in self.__dict__.items()
                  if not (isinstance(key, str) and key.startswith('_'))}
        params_list = f'{", ".join([f"{k}={params[k]}" for k in params])}'
        return f'{self.__class__.__name__}({params_list})'

    def run(self, context):
        raise NotImplementedError('Base class function Task.run() must not be called')

    def getarg(self, name, context={}, parse_jinja=True, parse_yaml=True, default=_SENTINEL):
        """Returns the value of argument 'name'.
           The argument value is parsed with Jinja2 and the given context, unless
           'parse_jinja' is False. The result is parsed once more with the YAML
           parser in order to get a correctly typed result. If parse_yaml is not
           True, the extra YAML parsing is skipped.
           Parsing with Jinja/YAML is also skipped, if the argument value is a
           string that starts with '_noparse_', '_noparsejinja_',
           '_noparseyaml_', respectively.
           If argument 'name' does not exist, the function raises an
           AttributeError, unless a 'default' value is given.
           """
        try:
            arg = getattr(self, name)

        except AttributeError:
            if default is _SENTINEL:
                raise AttributeError(f'Trying to access non-existing argument "{name}" '
                                     f'in "{self.__class__.__name__}"')
            arg = default

        if isinstance(arg, str):
            if parse_jinja and not isinstance(arg, scriptengine.yaml.NoParseJinjaString):
                # Make sure that a NoParseString is still a NoParseString after this!
                arg = type(arg)(scriptengine.jinja.render(arg, context))

            if parse_yaml and not isinstance(arg, scriptengine.yaml.NoParseYamlString):
                try:
                    arg = yaml.full_load(arg)
                except (yaml.scanner.ScannerError, yaml.parser.ParserError, yaml.constructor.ConstructorError):
                    self.log_debug(f'Reparsing argument "{arg}" with YAML failed')

            # For consistency, we always return plain strings
            if isinstance(arg, scriptengine.yaml.NoParseString):
                arg = str(arg)

        return arg

    def _log_message(self, message):
        return f'{message} [{str(self.id).split("-")[-1]}]'

    def log_debug(self, message):
        self._logger.debug(f'{message} ({self.id})')

    def log_info(self, message):
        self._logger.info(self._log_message(message))

    def log_warning(self, message):
        self._logger.warning(self._log_message(message))

    def log_error(self, message):
        self._logger.error(self._log_message(message))
