"""ScriptEngine YAML parsing
"""

import yaml
import dateutil.rrule
import logging

import scriptengine.tasks.core.loader
from scriptengine.jobs import Job
from scriptengine.exceptions import ScriptEngineParseFileError, \
                                    ScriptEngineParseScriptError, \
                                    ScriptEngineParseYAMLError


class NoParseYamlString(str):
    """This represents a string that should not be YAML-parsed"""


class NoParseJinjaString(str):
    """This represents a string that should not be parsed with Jinja2"""


class NoParseString(NoParseYamlString, NoParseJinjaString):
    """This represents a string that should not be parsed at all, neither YAML
       or Jinja2"""


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


yaml.add_constructor(u'!noparse',
                     string_class_constructor(NoParseString))
yaml.add_constructor(u'!noparse_yaml',
                     string_class_constructor(NoParseYamlString))
yaml.add_constructor(u'!noparse_jinja',
                     string_class_constructor(NoParseJinjaString))


def rrule_constructor(loader, node):
    """A YAML constructor that can parse RFC5545 rrules
    """
    value = loader.construct_scalar(node)
    rrule = dateutil.rrule.rrulestr(value)
    return rrule


yaml.add_constructor(u'!rrule', rrule_constructor)


def parse(data):
    """
    Args:
        data (dict or list of dicts): Data structure that holds the script
            description, i.e. job and task specifications. See the simple
            ScriptEngine grammar in the documentation.

    Returns:
        A scriptengine.task.Task, a scriptengine.jobs.Job, or a list of
        tasks/jobs.
    """

    if not data:
        return []

    tasks = scriptengine.tasks.core.loader.load_and_register()
    jobs = {"do"}

    # Recursively parse lists of tasks/jobs
    if isinstance(data, list):
        return [parse(item) for item in data]

    # Parse single task/job
    try:
        keys = (jobs | tasks.keys()) & data.keys()
    except AttributeError:
        logging.getLogger('se.yaml').error(
            'Expected YAML dictionary, got '
            f'"{type(data).__name__}: {data}"'
        )
        raise ScriptEngineParseScriptError
    if not keys:
        logging.getLogger('se.yaml').error(
            'Found unknown task name(s): '
            f'\"{", ".join(data.keys())}\"'
        )
        raise ScriptEngineParseScriptError
    if len(keys) > 1:
        logging.getLogger('se.yaml').error(
            'Found ambiguous task names: '
            f'\"{", ".join(data.keys())}\"'
        )
        raise ScriptEngineParseScriptError

    # There is exactly one key, get it
    key = keys.pop()

    if key in tasks:

        if '.' not in key:
            logging.getLogger('se.yaml').warn(
                f'Deprecation warning while processing task "{key}": '
                'The use of task names without dots (i.e. without a namespace)'
                f' is deprecated! This task defaults to "base.{key}", but the '
                'default will be removed in the future and an error will '
                'occur instead.'
            )

        if len(data) == 1:  # Simple task (no when clause or loop)
            return tasks[key](data[key])
        # Job made from single task with when/loop
        job = Job(when=data.get("when"), loop=data.get("loop"))
        job.append(parse({key: data[key]}))
        return job

    job = Job(when=data.get("when"), loop=data.get("loop"))
    for item in data[key]:
        job.append(parse(item))
    return job


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
    except (FileNotFoundError,
            PermissionError,
            IsADirectoryError) as e:
        logging.getLogger('se.yaml').error(
            f'Could not read script file: {e}'
        )
        raise ScriptEngineParseFileError
    except yaml.YAMLError as e:
        logging.getLogger('se.yaml').error(
            f'Could not parse script file: {e}'
        )
        raise ScriptEngineParseYAMLError
    return parse(data)
