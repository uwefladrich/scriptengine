from importlib import import_module

from scriptengine.exceptions import ScriptEngineError


_loaded_tasks = {}


def loaded_tasks():
    return _loaded_tasks.copy()


def load(modules):
    for mod_name in modules:
        try:
            module = import_module(mod_name)
        except ModuleNotFoundError:
            raise ScriptEngineError(
                        f'Taskset module "{mod_name}" not found')
        for task_name, task_class in module.task_loader_map().items():
            if task_name not in _loaded_tasks:
                _loaded_tasks[task_name] = task_class
            else:
                raise ScriptEngineError(
                        f'Duplicate task entry "{task_name}"'
                        f'from module "{mod_name}"')
