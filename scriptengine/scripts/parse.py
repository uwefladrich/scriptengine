"""ScriptEngine job parser.
"""

import re
import inspect
import yaml

import scriptengine.tasks
from scriptengine.jobs import Job

def camel_to_snake(string):
    """A small function that converts CamelCase strings to snake_case strings.
    Needed to convert class names to names used in the YAML syntax for ScriptEngine.

    See https://stackoverflow.com/questions/1175208 or
    https://gist.github.com/jaytaylor/3660565

    Could be performance-enhanced by storing the pre-compiled regexps.
    """
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()


def parse(data):
    """
    Args:
        data (dict or list of dicts): Data structure that holds the script
            description, i.e. job and task specifications. See the simple
            ScriptEngine grammar in the documentation.

    Returns:
        A scriptengine.task.Task, a scriptengine.jobs.Job, or a list of tasks/jobs.
    """
    tasks = {camel_to_snake(name):obj for name,obj in inspect.getmembers(scriptengine.tasks, inspect.isclass)}
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
        raise RuntimeError(f"Expected dictionary, got {type(data).__name__}: {data}")

    if not keys:
        raise RuntimeError(f"Unknown key: {list(data.keys())}")

    if len(keys)>1:
        raise RuntimeError(f"Ambiguous keys in {list(data.keys())}")

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


def parse_yaml_file(filename):
    """Reads a ScriptEngine script from a YAML file.

    Args:
        filename (str): Path to YAML file

    Returns:
        A scriptengine.task.Task, a scriptengine.jobs.Job, or a list of tasks/jobs.
    """
    with open(filename) as file:
        data = yaml.safe_load(file)
    return parse(data)
