from importlib import import_module

from scriptengine.exceptions import ScriptEngineStopException


_loaded_tasks = {}

def loaded_tasks():
    return _loaded_tasks.copy()

def load(modules):
    for mod_name in modules:
        module = import_module(mod_name)
        for task_name, task_class in module.task_loader_map().items():
            if task_name not in _loaded_tasks:
                _loaded_tasks[task_name] = task_class
            else:
                raise ScriptEngineStopException(f'Duplicate task entry "{task_name}"'
                                                f'from module "{mod_name}"')
