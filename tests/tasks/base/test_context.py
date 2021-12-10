import yaml

from scriptengine.context import ContextUpdate
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
    ctx = {}
    ctx_upd = t.run(ctx)
    ctx += ctx_upd
    assert type(ctx_upd) is ContextUpdate
    assert "foo" in ctx
    assert ctx["foo"] == 1


def test_context_simple_set():
    t = from_yaml(
        """
        base.context:
            foo: 1
            bar: 2
        """
    )
    ctx = {}
    ctx_upd = t.run(ctx)
    ctx += ctx_upd
    assert ctx["foo"] == 1
    assert ctx["bar"] == 2
