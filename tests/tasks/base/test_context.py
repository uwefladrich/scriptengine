import pytest
import yaml

from scriptengine.context import Context as SEContext
from scriptengine.exceptions import ScriptEngineTaskError, ScriptEngineTaskRunError
from scriptengine.tasks.base.context import Context as ContextTask
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_context_create():
    assert type(ContextTask({"foo": 1})) is ContextTask


def test_context_create_from_yaml():
    t = from_yaml(
        """
        base.context:
            foo: 1
    """
    )
    assert type(t) is ContextTask


def test_context_run_returns_dict():
    t = from_yaml(
        """
        base.context:
            foo: 1
        """
    )
    ctx = SEContext()
    ctx_upd = t.run(ctx)
    ctx += ctx_upd
    assert type(ctx_upd) is SEContext
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
    ctx = t.run(SEContext())
    assert ctx["foo"] == 1
    assert ctx["bar"] == 2


def test_context_load_dict():
    t = from_yaml(
        """
        base.context.load:
            dict: {'foo': 1, 'bar': 2}
        """
    )
    ctx = t.run(SEContext())
    assert ctx["foo"] == 1
    assert ctx["bar"] == 2


def test_context_load_context_dict():
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
        base.context.load:
            dict: '{{update}}'
        """
    )
    ctx = SEContext()
    ctx += t1.run(ctx)
    ctx += t2.run(ctx)
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
        base.context.load:
            dict: '{{update}}'
        """
    )
    ctx = SEContext()
    ctx += t1.run(ctx)
    ctx += t2.run(ctx)
    ctx += t3.run(ctx)
    assert ctx["foo"] == 5
    assert ctx["bar"] == 2


def test_context_load_file(tmp_path):
    f = tmp_path / "f.yml"
    f.write_text(
        """
        foo: 1
        bar: 2
        """
    )
    t = from_yaml(
        f"""
        base.context.load:
            file: {f}
        """
    )
    ctx = t.run(SEContext())
    assert ctx["foo"] == 1
    assert ctx["bar"] == 2


def test_context_load_no_args():
    t = from_yaml(
        """
        base.context.load:
        """
    )
    with pytest.raises(ScriptEngineTaskError):
        t.run(SEContext())


def test_context_load_double_args():
    t = from_yaml(
        """
        base.context.load:
            dict: foo
            file: bar
        """
    )
    with pytest.raises(ScriptEngineTaskError):
        t.run(SEContext())


def test_context_load_dict_not_a_dict():
    t = from_yaml(
        """
        base.context.load:
            dict: [1, 2, 3]
        """
    )
    with pytest.raises(ScriptEngineTaskRunError):
        t.run(SEContext())


def test_context_load_file_not_found():
    t = from_yaml(
        """
        base.context.load:
            file: foo
        """
    )
    with pytest.raises(ScriptEngineTaskRunError):
        t.run(SEContext())


def test_context_load_file_not_yaml(tmp_path):
    f = tmp_path / "f.yml"
    f.write_text(
        """
        @@@
        """
    )
    t = from_yaml(
        f"""
        base.context.load:
            file: {f}
        """
    )
    with pytest.raises(ScriptEngineTaskRunError):
        t.run(SEContext())


def test_context_load_file_not_dict(tmp_path):
    f = tmp_path / "f.yml"
    f.write_text(
        """
        - foo
        - bar
        """
    )
    t = from_yaml(
        f"""
        base.context.load:
            file: {f}
        """
    )
    with pytest.raises(ScriptEngineTaskRunError):
        t.run(SEContext())
