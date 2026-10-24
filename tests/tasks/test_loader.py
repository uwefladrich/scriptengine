from importlib.metadata import EntryPoint
import pytest

from scriptengine.exceptions import ScriptEngineTaskLoaderError
from scriptengine.tasks.core import Task
from scriptengine.tasks.core import loader
from scriptengine.yaml.parser import parse


def test_lazy_load(monkeypatch):
    loaded = []
    orig_load = EntryPoint.load

    def tracked_load(self):
        loaded.append(self.name)
        return orig_load(self)

    monkeypatch.setattr(EntryPoint, "load", tracked_load)

    loader.load.cache_clear()
    tasks = loader.load()

    assert "base.echo" in tasks
    assert len(tasks) > 0
    assert "base.echo" in tasks.keys()
    assert loaded == []

    task_cls = tasks["base.echo"]
    assert issubclass(task_cls, Task)
    assert task_cls._reg_name == "base.echo"
    assert loaded == ["base.echo"]


def test_clash_detection(monkeypatch):
    ep1 = EntryPoint(name="clash.task", value="mod1:Task1", group="scriptengine.tasks")
    ep2 = EntryPoint(name="clash.task", value="mod2:Task2", group="scriptengine.tasks")

    def fail_load(self):
        raise AssertionError("Module must not be loaded during clash detection")

    monkeypatch.setattr(EntryPoint, "load", fail_load)
    monkeypatch.setattr(loader, "_task_entry_points", lambda: [ep1, ep2])

    loader.load.cache_clear()
    with pytest.raises(ScriptEngineTaskLoaderError):
        loader.load()


def test_parse_only_loads_used_tasks(monkeypatch):
    loaded = []
    orig_load = EntryPoint.load

    def tracked_load(self):
        loaded.append(self.name)
        return orig_load(self)

    monkeypatch.setattr(EntryPoint, "load", tracked_load)

    loader.load.cache_clear()
    script = parse({"base.echo": {"msg": "hello"}})
    assert script is not None
    assert loaded == ["base.echo"]
