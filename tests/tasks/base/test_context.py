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


def test_context_from_dict():
    t = from_yaml(
        """
        base.context.from:
            dict: {'foo': 1, 'bar': 2}
        """
    )
    ctx = {}
    ctx_upd = t.run(ctx)
    ctx += ctx_upd
    assert ctx["foo"] == 1
    assert ctx["bar"] == 2


def test_context_from_context_dict():
    t1 = from_yaml(
        """
        base.context:
            update:
                foo: 1
                bar: 2
        """
    )
    t2 = from_yaml(
        """
        base.context.from:
            dict: '{{update}}'
        """
    )
    ctx = {}
    ctx_upd = t1.run(ctx)
    ctx += ctx_upd
    ctx_upd = t2.run(ctx)
    ctx += ctx_upd
    assert ctx["foo"] == 1
    assert ctx["bar"] == 2


def test_context_update_from_context_dict():
    t1 = from_yaml(
        """
        base.context:
            update:
                foo: 5
        """
    )
    t2 = from_yaml(
        """
        base.context:
            foo: 1
            bar: 2
        """
    )
    t3 = from_yaml(
        """
        base.context.from:
            dict: '{{update}}'
        """
    )
    ctx = {}
    ctx_upd = t1.run(ctx)
    ctx += ctx_upd
    ctx_upd = t2.run(ctx)
    ctx += ctx_upd
    ctx_upd = t3.run(ctx)
    ctx += ctx_upd
    assert ctx["foo"] == 5
    assert ctx["bar"] == 2


def test_context_from_file(tmp_path):
    f = tmp_path / "f.yml"
    f.write_text(
        """
        foo: 1
        bar: 2
        """
    )
    t = from_yaml(
        f"""
        base.context.from:
            file: {f}
        """
    )
    ctx = {}
    ctx_upd = t.run(ctx)
    ctx += ctx_upd
    assert ctx["foo"] == 1
    assert ctx["bar"] == 2
