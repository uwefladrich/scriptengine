"""ScriptEngine job parser.
"""

import inspect
import yaml

import se.tasks
from se.jobs import Job


def from_dict(data):
    """
    Args:
        data (dict): a dictionary holding the job specs

    Returns:
        the created job of type se.jobs.Job
    """
    tasks = {name.lower():obj for name,obj in inspect.getmembers(se.tasks, inspect.isclass)}
    jobs  = {'do'}

    next_keys = (set(tasks)|jobs).intersection(data)

    if not next_keys:
        raise RuntimeError(f"Unknown key in {data}")

    if len(next_keys)>1:
        raise RuntimeError(f"Ambiguous keys in {data}")

    key = next_keys.pop()

    if key in tasks:
        if len(data)==1: # Simple task
            return tasks[key](data[key])
        else:            # Job made of a single task
            job = Job(when=data.get("when"), loop=data.get("loop"))
            job.append(from_dict({key: data[key]}))
            return job
    else:
        job = Job(when=data.get("when"), loop=data.get("loop"))
        for j in data[key]:
            job.append(from_dict(j))
        return job

def from_yaml_file(filename):
    """Reads jobs from YAML file.

    Args:
        filename (str): Path to YAML file

    Returns:
        job or list of jobs
    """
    with open(filename) as file:
        data = yaml.safe_load(file)

    job = Job()
    for d in data if isinstance(data, list) else [data]:
        job.append(from_dict(d))
    return job
