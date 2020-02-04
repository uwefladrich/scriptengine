"""ScriptEngine task module.

Provides the base class for all tasks.
"""

import logging
import uuid


class Task:

    def __init__(self, logger_name, parameters=None, required_parameters=None):

        self._identifier = uuid.uuid4()

        if "run" in (parameters or []):
            raise RuntimeError(f"Reserved identifier 'run' used as parameter while creating task")
        self.__dict__.update(parameters or {})

        for param in (required_parameters or []):
            if param not in self.__dict__:
                raise RuntimeError(f"Missing required parameter '{param}' while creating "
                                   f"'{type(self).__name__}' task from {parameters!s}")
        self._logger = logging.getLogger(logger_name)
        self.log_debug(f"Create '{type(self).__name__}' task from {parameters!s}")

    @property
    def id(self):
        return self._identifier

    def __repr__(self):
        my_params = {key: value for key, value in self.__dict__.items()
                     if key[0] != "_"}
        return f"{self.__class__.__name__}({my_params})"

    def run(self, context):
        raise NotImplementedError(f"Base class function Task.run() must not be called")

    def log_debug(self, message):
        self._logger.debug(f"{message} ({self.id})")

    def log_info(self, message):
        self._logger.info(f"{message} ({self.id})")

    def log_warning(self, message):
        self._logger.warning(f"{message} ({self.id})")

    def log_error(self, message):
        self._logger.error(f"{message} ({self.id})")
