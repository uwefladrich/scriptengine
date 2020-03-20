"""ScriptEngine YAML parsing
"""

import yaml
import dateutil.rrule

import scriptengine.tasks
from scriptengine.jobs import Job
from scriptengine.exceptions import ScriptEngineStopException


def construct_noeval_string(loader, node):
    value = loader.construct_scalar(node)
    return f"_noeval_{str(value)}"
yaml.add_constructor(u"!noeval", construct_noeval_string)


def construct_rrule(loader, node):
    value = loader.construct_scalar(node)
    rrule = dateutil.rrule.rrulestr(value)
    return rrule
yaml.add_constructor(u"!rrule", construct_rrule)


def parse(data):
    """
    Args:
        data (dict or list of dicts): Data structure that holds the script
            description, i.e. job and task specifications. See the simple
            ScriptEngine grammar in the documentation.

    Returns:
        A scriptengine.task.Task, a scriptengine.jobs.Job, or a list of tasks/jobs.
    """
    tasks = scriptengine.tasks.loader.loaded
    jobs  = {"do"}

    if not data:
        return []

    if isinstance(data, list):
        result = []
        for item in data:
            result.append(parse(item))
        return result

    # Parse and return a single task or job
    try:
        keys = (jobs|tasks.keys()) & data.keys()
    except AttributeError:
        raise ScriptEngineStopException(f"Expected dictionary, got "
                                        f"{type(data).__name__}: {data}")
    if not keys:
        raise ScriptEngineStopException(f"Unknown task name in: "
                                        f"{list(data.keys())}")
    if len(keys)>1:
        raise ScriptEngineStopException(f"Ambiguous keys in "
                                        f"{list(data.keys())}")

    key = keys.pop()

    if key in tasks:
        if len(data)==1: # Simple task (no when clause or loop)
            return tasks[key](data[key])
        else:            # Job made from single task with when/loop
            job = Job(when=data.get("when"), loop=data.get("loop"))
            job.append(parse({key: data[key]}))
            return job
    else:
        job = Job(when=data.get("when"), loop=data.get("loop"))
        for item in data[key]:
            job.append(parse(item))
        return job


def parse_file(filename):
    """Reads a ScriptEngine script from a YAML file.

    Args:
        filename (str): Path to YAML file

    Returns:
        A scriptengine.task.Task, a scriptengine.jobs.Job, or a list of tasks/jobs.
    """
    with open(filename) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return parse(data)
