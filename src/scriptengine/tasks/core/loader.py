import collections.abc
import functools
import logging

try:
    from importlib.metadata import entry_points
except ModuleNotFoundError:  # Python prior to 3.8
    from importlib_metadata import entry_points

from scriptengine.exceptions import ScriptEngineTaskLoaderError


class _LazyTaskMap(collections.abc.Mapping):
    """Lazy mapping for ScriptEngine tasks.

    Discovers task entry points without importing task modules.
    Task modules are only loaded when accessed by name.
    """

    def __init__(self, entry_points):
        self._eps = entry_points
        self._loaded = {}

    def __getitem__(self, name):
        if name not in self._eps:
            raise KeyError(name)
        if name not in self._loaded:
            task = self._eps[name].load()
            task.register_name(name)
            self._loaded[name] = task
            logging.getLogger("se.task.loader").debug(
                f"Loaded task {name}: {task.__name__} from {task.__module__}"
            )
        return self._loaded[name]

    def __contains__(self, name):
        return name in self._eps

    def __iter__(self):
        return iter(self._eps)

    def __len__(self):
        return len(self._eps)


def _task_entry_points():
    try:
        return list(entry_points(group="scriptengine.tasks"))
    except TypeError:  # importlib.metadata prior to Python 3.10
        return list(entry_points().get("scriptengine.tasks", []))


def _discover_tasks():
    discovered = {}
    for ep in _task_entry_points():
        if ep.name not in discovered:
            discovered[ep.name] = ep
        else:
            existing_ep = discovered[ep.name]
            existing_mod = existing_ep.value.partition(":")[0]
            clashing_mod = ep.value.partition(":")[0]
            logging.getLogger("se.task.loader").error(
                f'Same task name "{ep.name}" defined in modules '
                f'"{existing_mod}" and "{clashing_mod}"'
            )
            raise ScriptEngineTaskLoaderError
    return discovered


@functools.lru_cache(maxsize=None)
def load():
    """Return the lazily populated mapping of available tasks.

    Entry points are discovered once and cached. Task modules are imported
    and registered under their entry-point name only when that name is first
    accessed through the returned mapping, so unused tasks do not incur
    import costs.

    Because discovery is cached, tasks installed or added dynamically after
    the first call are not picked up in the same process.
    """
    return _LazyTaskMap(_discover_tasks())
