"""ScriptEngine task module.

Provides the base class for all tasks.
"""

import logging
import uuid

class Task:

    def __init__(self, logger_name, parameters, required_parameters=[]):

        self._identifier = uuid.uuid4()

        if "run" in parameters:
            raise RuntimeError(f"Reserved identifier 'run' used as parameter while creating task")
        self.__dict__.update(parameters)

        for param in required_parameters:
            if param not in self.__dict__:
                raise RuntimeError(f"Missing required parameter '{param}' while creating task")

        self._logger = logging.getLogger(logger_name)
        self.log_debug(f"Created Task from {parameters!s}")

    @property
    def id(self):
        return self._identifier

    def __repr__(self):
        my_params = {key: value for key, value in self.__dict__.items()
                                                        if key[0]!="_"}
        return f"{self.__class__.__name__}({my_params})"

    def run(self, context):
        raise NotImplementedError(f"Base class function Task.run() must not be called")

    def log_debug(self, message):
        self._logger.debug(message)

    def log_info(self, message):
        self._logger.info(message)

    def log_warning(self, message):
        self._logger.warning(message)

    def log_error(self, message):
        self._logger.error(message)
