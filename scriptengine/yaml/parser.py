"""ScriptEngine YAML parsing
"""

import logging

import dateutil.rrule
import yaml

from scriptengine.exceptions import (
    ScriptEngineParseFileError,
    ScriptEngineParseScriptError,
    ScriptEngineParseYAMLError,
)
from scriptengine.jobs import Job
from scriptengine.tasks.core.loader import load_and_register
from scriptengine.yaml.noparse_strings import (
    NoParseJinjaString,
    NoParseString,
    NoParseYamlString,
)


def string_class_constructor(derived_string_class):
    """YAML constructor factory. The constructors convert their values to a
    string and return an object of a specific class (derived from str). The
    class membership is later used to limit the Jinja2/YAML parsing during
    the processing of ScriptEngine scripts.
    """

    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return derived_string_class(str(value))

    return constructor


yaml.add_constructor("!noparse", string_class_constructor(NoParseString))
yaml.add_constructor("!noparse_yaml", string_class_constructor(NoParseYamlString))
yaml.add_constructor("!noparse_jinja", string_class_constructor(NoParseJinjaString))


def rrule_constructor(loader, node):
    """A YAML constructor that can parse RFC5545 rrules"""
    value = loader.construct_scalar(node)
    rrule = dateutil.rrule.rrulestr(value)
    return rrule


yaml.add_constructor("!rrule", rrule_constructor)


def parse(data):
    """Recursively parses data and returns a ScriptEnginge Task or Job, or a list of those.
    The data is supposed to come from YAML-parsing a ScriptEngine script."""

    def build_job(todo, spec):
        sentinel = object()

        when_clause = spec.get("when")
        loop_descriptor = spec.get("loop", sentinel)

        loop_opts = {}
        if loop_descriptor is not sentinel:
            if not loop_descriptor:
                log.error(
                    f"Invalid loop descriptor (evaluates to False): {loop_descriptor}"
                )
                raise ScriptEngineParseYAMLError
            if isinstance(loop_descriptor, list) or isinstance(loop_descriptor, str):
                loop_opts = {
                    "loop": loop_descriptor,
                    "loop_vars": None,
                }
            elif isinstance(loop_descriptor, dict) and "in" in loop_descriptor:
                loop_opts = {
                    "loop": loop_descriptor["in"],
                    "loop_vars": loop_descriptor.get("with"),
                }
            else:
                log.error(f"Invalid loop descriptor: {loop_descriptor}")
                raise ScriptEngineParseYAMLError
        return Job(todo, when=when_clause, **loop_opts)

    if not data:
        return []

    if isinstance(data, list):
        return [parse(d) for d in data]

    log = logging.getLogger("se.yaml")

    tasks = load_and_register()
    job_keys = {"do"}

    try:
        valid_keys = data.keys() & (job_keys | tasks.keys())
    except AttributeError:
        log.error(f"Expected YAML list or dict, got {type(data).__name__}: {data}")
        raise ScriptEngineParseScriptError

    if not valid_keys:
        log.error(f"No valid task name found in {data.keys()}")
        raise ScriptEngineParseScriptError

    if len(valid_keys) > 1:
        log.error(f"Ambiguous task names found in {data.keys()}")
        raise ScriptEngineParseScriptError

    key = valid_keys.pop()

    if key in tasks:
        if len(data) == 1:  # It's a simple Task
            return tasks[key](data[key])
        return build_job(parse({key: data[key]}), data)

    return build_job(
        [parse(t) for t in data[key]],
        data,
    )


def parse_file(filename):
    """Reads a ScriptEngine script from a YAML file.

    Args:
        filename (str): Path to YAML file

    Returns:
        A scriptengine.task.Task, a scriptengine.jobs.Job, or a list of
        tasks/jobs.
    """
    try:
        with open(filename) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
    except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
        logging.getLogger("se.yaml").error(f"Could not read script file: {e}")
        raise ScriptEngineParseFileError
    except yaml.YAMLError as e:
        logging.getLogger("se.yaml").error(f"Could not parse script file: {e}")
        raise ScriptEngineParseYAMLError
    return parse(data)
