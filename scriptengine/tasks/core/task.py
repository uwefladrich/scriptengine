"""ScriptEngine task module.

Provides the base class for all tasks.
"""

import logging
import uuid
import yaml

import scriptengine.jinja
import scriptengine.yaml

from scriptengine.exceptions import ScriptEngineTaskArgumentError, \
                                    ScriptEngineTaskArgumentInvalidError, \
                                    ScriptEngineTaskArgumentMissingError


_SENTINEL = object()


class Task:

    _invalid_arguments = ('run', 'id', '_logger', )

    @classmethod
    def check_arguments(cls, arguments):
        """Checks arguments against class members '_invalid_arguments' and
        '_required_arguments', if present. Returns None or throws either
        ScriptEngineTaskArgumentInvalidError or
        ScriptEngineTaskArgumentMissingError.
        """
        for name in arguments:
            if name in getattr(cls, '_invalid_arguments', ()):
                logmsg = (f'Invalid argument "{name}" found while '
                          f'trying to create {cls.__name__} task')
                logging.getLogger('se.task').error(logmsg, extra={'id': None})
                raise ScriptEngineTaskArgumentInvalidError(logmsg)
        for name in getattr(cls, '_required_arguments', ()):
            if name not in arguments:
                logmsg = (f'Missing required argument "{name}" while '
                          f'trying to create {cls.__name__} task')
                logging.getLogger('se.task').error(logmsg, extra={'id': None})
                raise ScriptEngineTaskArgumentMissingError(logmsg)

    def __init__(self, arguments=None):

        self._identifier = uuid.uuid4()

        if arguments is not None:
            try:
                Task.check_arguments(arguments)
            except ScriptEngineTaskArgumentError as e:
                self.log_error(e)
                raise
            for name, value in arguments.items():
                if hasattr(self, name):
                    self.log_error(f'Invalid task argument (reserved): {name}')
                    raise ScriptEngineTaskArgumentInvalidError(
                                   f'Invalid task argument (reserved): {name}')
                setattr(self, name, value)
        self.log_debug(f'Created task: {self}')

    @property
    def id(self):
        return self._identifier

    @property
    def shortid(self):
        return self._identifier.hex[:10]

    def __repr__(self):
        params = {key: val for key, val in self.__dict__.items()
                  if not (isinstance(key, str) and key.startswith('_'))}
        params_list = f'{", ".join([f"{k}={params[k]}" for k in params])}'
        return f'{self.__class__.__name__}({params_list})'

    def run(self, context):
        raise NotImplementedError('Base class function Task.run() '
                                  'must not be called')

    def getarg(self, name, context={},
               parse_jinja=True, parse_yaml=True, default=_SENTINEL):
        """Returns the value of argument 'name'.
           The argument value is parsed with Jinja2 and the given context,
           unless 'parse_jinja' is False. The result is parsed once more with
           the YAML parser in order to get a correctly typed result. If
           parse_yaml is not True, the extra YAML parsing is skipped.
           Parsing with Jinja/YAML is also skipped, if the argument value is a
           string that starts with '_noparse_', '_noparsejinja_',
           '_noparseyaml_', respectively.
           If argument 'name' does not exist, the function raises an
           AttributeError, unless a 'default' value is given.
           """

        def parse(arg_):

            # Recursively parse list items
            if isinstance(arg_, list):
                return [parse(item) for item in arg_]

            # Recursively parse dict values (not keys!)
            if isinstance(arg_, dict):
                return dict((key, parse(val)) for key, val in arg_.items())

            if isinstance(arg_, str):
                if parse_jinja and \
                   not isinstance(arg_, scriptengine.yaml.NoParseJinjaString):
                    # Make sure that a NoParseString is still a NoParseString
                    # after this!
                    arg_ = type(arg_)(scriptengine.jinja.render(arg_, context))

                if parse_yaml and \
                   not isinstance(arg_, scriptengine.yaml.NoParseYamlString):
                    try:
                        return yaml.full_load(arg_)
                    except (yaml.scanner.ScannerError,
                            yaml.parser.ParserError,
                            yaml.constructor.ConstructorError):
                        self.log_debug(f'Reparsing argument "{arg_}" '
                                       'with YAML failed')

                # Return plain strings, not NoParse*Strings
                return str(arg_)

            # If not a list, dict or string, just return
            return arg_

        try:
            arg = getattr(self, name)

        except AttributeError:
            if default is _SENTINEL:
                self.log_error(f'Missing task argument: {name}')
                raise ScriptEngineTaskArgumentMissingError(
                                        f'Missing task argument: {name}')
            arg = default

        return parse(arg)

    def _log(self, level, msg):
        logger = getattr(self, '_logger',
                         'se.task.'+self.__class__.__name__.lower())
        logging.getLogger(logger).log(level, msg, extra={'id': self.shortid})

    def log_debug(self, msg):
        self._log(logging.DEBUG, msg)

    def log_info(self, msg):
        self._log(logging.INFO, msg)

    def log_warning(self, msg):
        self._log(logging.WARNING, msg)

    def log_error(self, msg):
        self._log(logging.ERROR, msg)

    def log_critical(self, msg):
        self._log(logging.CRITICAL, msg)
