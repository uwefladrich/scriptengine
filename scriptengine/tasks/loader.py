from importlib import import_module

from scriptengine.exceptions import ScriptEngineStopException

loaded = {}

def load(modules):
    for name in modules:
        mod = import_module(name)
        for tname, tclass in mod.taskmap().items():
            if tname in loaded:
                raise ScriptEngineStopException(f"Duplicate task entry: {tname} "
                                                f"from {name}")
            else:
                loaded[tname] = tclass
