"""ScriptEngine exceptions
"""


class ScriptEngineStopException(Exception):
    """Raise this exception when ScriptEngine should stop"""


class ScriptEngineError(Exception):
    """All ScriptEngine errors should throw this"""


class ScriptEngineParseError(ScriptEngineError):
    """An error that has to do with parsing SE scripts"""


class ScriptEngineParseFileError(ScriptEngineParseError):
    """An file error while acessing an SE script"""


class ScriptEngineParseJinjaError(ScriptEngineParseError):
    """Throw this exception whenever there is a problem with parsing Jinja2
    expressions"""


class ScriptEngineParseYAMLError(ScriptEngineParseError):
    """Throw this exception whenever there is a problem with parsing YAML"""


class ScriptEngineParseScriptError(ScriptEngineParseError):
    """Throw this exception if YAML/Jinja2 is okay, but the result can not be
    parsed as a valid ScriptEngine script"""


class ScriptEngineTaskError(ScriptEngineError):
    """All ScriptEngine Tasks should throw this"""


class ScriptEngineTaskLoaderError(ScriptEngineTaskError):
    """There is a problem while loading an SE task or taskset"""


class ScriptEngineTaskArgumentError(ScriptEngineTaskError):
    """There is a problem with an SE Task argument"""


class ScriptEngineTaskArgumentInvalidError(ScriptEngineTaskArgumentError):
    """An SE Task argument is not valid"""


class ScriptEngineTaskArgumentMissingError(ScriptEngineTaskArgumentError):
    """An SE Task argument is missing"""


class ScriptEngineTaskRunError(ScriptEngineTaskError):
    """Throw this for errors at run time, i.e. during execution of the tasks
    run() method"""


class ScriptEngineJobError(ScriptEngineError):
    """All ScriptEngine Jobs should throw this"""


class ScriptEngineJobParseError(ScriptEngineJobError):
    """An error while parsing a job description"""
