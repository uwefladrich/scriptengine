import yaml

from scriptengine.tasks.base.context import Context
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_context_create():
    assert type(Context({"foo": 1})) is Context


def test_context_create_from_yaml():
    t = from_yaml(
        """
        base.context:
            foo: 1
    """
    )
    assert type(t) is Context


def test_context_run_returns_dict():
    t = from_yaml(
        """
        base.context:
            foo: 1
        """
    )
    d = t.run({})
    assert type(d) is dict
    assert "foo" in d
    assert d["foo"] == 1


def test_context_simple_set():
    t = from_yaml(
        """
        base.context:
            foo: 1
            bar: 2
        """
    )
    c = t.run({})
    assert c["foo"] == 1
    assert c["bar"] == 2
