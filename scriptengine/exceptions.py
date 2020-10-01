"""ScriptEngine exceptions
"""


class ScriptEngineStopException(Exception):
    """Raise this exception when ScriptEngine should stop"""


class ScriptEngineError(Exception):
    """All ScriptEngine errors should throw this"""


class ScriptEngineTaskError(ScriptEngineError):
    """All ScriptEngine Tasks should throw this"""


class ScriptEngineTaskArgumentError(ScriptEngineTaskError):
    """There is a problem with an SE Task argument"""


class ScriptEngineTaskArgumentInvalidError(ScriptEngineTaskArgumentError):
    """An SE Task argument is not valid"""


class ScriptEngineTaskArgumentMissingError(ScriptEngineTaskArgumentError):
    """An SE Task argument is missing"""
