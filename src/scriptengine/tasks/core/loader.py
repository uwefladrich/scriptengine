import functools
import logging

try:
    from importlib.metadata import entry_points
except ModuleNotFoundError:  # Python prior to 3.8
    from importlib_metadata import entry_points

from scriptengine.exceptions import ScriptEngineTaskLoaderError


# The load function goes through entry points, searching for ScriptEngine
# tasks. Since the function can be called quite frequently and modules are
# *usually* not loaded while SE is run, the result is cached.
# Note that this means that dynamic module is *not supported* by the loading
# mechanism!
@functools.lru_cache(maxsize=None)
def load():
    loaded_tasks = dict()
    try:
        eps = entry_points(group="scriptengine.tasks")
    except TypeError:  # importlib.metadata prior to Python 3.10
        eps = set(entry_points().get("scriptengine.tasks", []))
    for ep in eps:
        if ep.name not in loaded_tasks:
            loaded_tasks[ep.name] = ep.load()
        else:
            existing_ep = next(cep for cep in eps if cep.name == ep.name)
            existing_mod = existing_ep.value.partition(":")[0]
            clashing_mod = ep.value.partition(":")[0]
            logging.getLogger("se.task.loader").error(
                f'Same task name "{ep.name}" defined in modules '
                f'"{existing_mod}" and "{clashing_mod}"'
            )
            raise ScriptEngineTaskLoaderError

    return loaded_tasks


def load_and_register():
    loaded_tasks = load()
    for name, task in loaded_tasks.items():
        task.register_name(name)
    return loaded_tasks
