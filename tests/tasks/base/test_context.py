import pytest
import yaml

from scriptengine.context import Context as SEContext
from scriptengine.engines import SimpleScriptEngine
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


def test_context_dump_file(tmp_path):
    f = tmp_path / "f.yml"
    t1 = from_yaml(
        """
        base.context:
            foo: 1
            bar: 2
        """
    )
    t2 = from_yaml(
        f"""
        base.context.dump:
            file: {f}
        """
    )
    ctx = SEContext()
    ctx += t1.run(ctx)
    t2.run(ctx)
    assert f.exists()
    assert yaml.safe_load(f.read_text()) == {"foo": 1, "bar": 2}


def test_context_dump_keys(tmp_path):
    f = tmp_path / "f.yml"
    t1 = from_yaml(
        """
        base.context:
            foo: 1
            bar: 2
            baz: 3
        """
    )
    t2 = from_yaml(
        f"""
        base.context.dump:
            file: {f}
            keys:
                - foo
                - bar
        """
    )
    ctx = SEContext()
    ctx += t1.run(ctx)
    t2.run(ctx)
    assert f.exists()
    assert yaml.safe_load(f.read_text()) == {"foo": 1, "bar": 2}


def test_context_dump_root(tmp_path):
    f = tmp_path / "f.yml"
    t1 = from_yaml(
        """
        base.context:
            foo: 1
            bar: 2
        """
    )
    t2 = from_yaml(
        f"""
        base.context.dump:
            file: {f}
            root: ic_meta
            keys:
                - foo
        """
    )
    ctx = SEContext()
    ctx += t1.run(ctx)
    t2.run(ctx)
    assert f.exists()
    assert yaml.safe_load(f.read_text()) == {"ic_meta": {"foo": 1}}


def test_context_dump_no_args():
    t = from_yaml(
        """
        base.context.dump:
        """
    )
    with pytest.raises(ScriptEngineTaskError):
        t.run(SEContext())


def test_context_dump_keys_string(tmp_path):
    f = tmp_path / "f.yml"
    t1 = from_yaml(
        """
        base.context:
            foo: 1
            bar: 2
        """
    )
    t2 = from_yaml(
        f"""
        base.context.dump:
            file: {f}
            keys: foo
        """
    )
    ctx = SEContext()
    ctx += t1.run(ctx)
    t2.run(ctx)
    assert f.exists()
    assert yaml.safe_load(f.read_text()) == {"foo": 1}


def test_context_dump_keys_invalid_type(tmp_path):
    f = tmp_path / "f.yml"
    t = from_yaml(
        f"""
        base.context.dump:
            file: {f}
            keys:
                a: 1
        """
    )
    with pytest.raises(ScriptEngineTaskRunError):
        t.run(SEContext())


def test_context_setdefault_basic():
    t = from_yaml(
        """
        base.context.setdefault:
            foo: 1
            bar: "two"
        """
    )
    upd = t.run(SEContext())
    assert upd["foo"] == 1
    assert upd["bar"] == "two"


def test_context_setdefault_preserves_existing():
    t = from_yaml(
        """
        base.context.setdefault:
            foo: 999
            bar: "new"
        """
    )
    upd = t.run(SEContext({"foo": 1}))
    assert "foo" not in upd
    assert upd["bar"] == "new"


def test_context_setdefault_nested_issue_127():
    t = from_yaml(
        """
        base.context.setdefault:
            experiment:
                timestep: 900
                name: "standard_run"
        """
    )
    ctx = SEContext({"experiment": {"timestep": 450}})
    upd = t.run(ctx)
    ctx += upd
    assert ctx["experiment"]["timestep"] == 450
    assert ctx["experiment"]["name"] == "standard_run"


def test_context_setdefault_dotted_keys():
    t = from_yaml(
        """
        base.context.setdefault:
            "experiment.timestep": 900
            "experiment.name": "standard_run"
        """
    )
    ctx = SEContext({"experiment": {"timestep": 450}})
    upd = t.run(ctx)
    ctx += upd
    assert ctx["experiment"]["timestep"] == 450
    assert ctx["experiment"]["name"] == "standard_run"


def test_context_setdefault_lazy_evaluation():
    # If a key already exists, its default value must NOT be evaluated
    # (even if it contains unresolvable Jinja expressions)
    t = from_yaml(
        """
        base.context.setdefault:
            existing_var: "{{ undefined_variable | non_existent_filter }}"
            missing_var: "computed_{{ existing_var }}"
        """
    )
    ctx = SEContext({"existing_var": "val"})
    upd = t.run(ctx)
    ctx += upd
    assert ctx["existing_var"] == "val"
    assert ctx["missing_var"] == "computed_val"


def test_context_setdefault_preserves_lists():
    t = from_yaml(
        """
        base.context.setdefault:
            model:
                components: ["oifs", "nemo"]
                version: 4
        """
    )
    ctx = SEContext({"model": {"components": ["oifs"]}})
    upd = t.run(ctx)
    ctx += upd
    assert ctx["model"]["components"] == ["oifs"]
    assert ctx["model"]["version"] == 4


def test_context_setdefault_in_engine():
    s = from_yaml(
        """
        - base.context:
            experiment:
                timestep: 450
        - base.context.setdefault:
            experiment:
                timestep: 900
                name: "standard_run"
            extra: "value"
        """
    )
    res = SimpleScriptEngine().run(s, context=SEContext())
    assert res["experiment"]["timestep"] == 450
    assert res["experiment"]["name"] == "standard_run"
    assert res["extra"] == "value"


def test_context_set_alias():
    s = from_yaml(
        """
        - base.context.set:
            foo: 1
            bar.baz: 2
        """
    )
    res = SimpleScriptEngine().run(s, context=SEContext())
    assert res["foo"] == 1
    assert res["bar"]["baz"] == 2


def test_context_setdefault_preserves_none():
    t = from_yaml(
        """
        base.context.setdefault:
            foo: 999
            bar: "default"
        """
    )
    ctx = SEContext({"foo": None})
    upd = t.run(ctx)
    ctx += upd
    assert ctx["foo"] is None
    assert ctx["bar"] == "default"


def test_context_default_basic_and_populates_none():
    t = from_yaml(
        """
        base.context.default:
            foo: 999
            bar: "default_bar"
            baz: "default_baz"
        """
    )
    ctx = SEContext({"foo": None, "bar": "custom_bar"})
    upd = t.run(ctx)
    ctx += upd
    assert ctx["foo"] == 999
    assert ctx["bar"] == "custom_bar"
    assert ctx["baz"] == "default_baz"


def test_context_default_preserves_falsy_non_none():
    t = from_yaml(
        """
        base.context.default:
            f_bool: true
            f_zero: 10
            f_str: "filled"
            f_list: [1, 2]
        """
    )
    ctx = SEContext({"f_bool": False, "f_zero": 0, "f_str": "", "f_list": []})
    upd = t.run(ctx)
    ctx += upd
    assert ctx["f_bool"] is False
    assert ctx["f_zero"] == 0
    assert ctx["f_str"] == ""
    assert ctx["f_list"] == []


def test_context_default_nested_null():
    t = from_yaml(
        """
        base.context.default:
            experiment:
                timestep: 900
                name: "standard_run"
        """
    )
    # Skeleton config where experiment is defined with timestep as null
    ctx = SEContext({"experiment": {"timestep": None}})
    upd = t.run(ctx)
    ctx += upd
    assert ctx["experiment"]["timestep"] == 900
    assert ctx["experiment"]["name"] == "standard_run"


def test_context_default_in_engine():
    s = from_yaml(
        """
        - base.context:
            model_config:
                output_cfg: null
                components: ["oifs"]
        - base.context.default:
            model_config:
                output_cfg: "presets/output.yml"
                components: ["oifs", "nemo"]
                version: 4
        """
    )
    res = SimpleScriptEngine().run(s, context=SEContext())
    assert res["model_config"]["output_cfg"] == "presets/output.yml"
    assert res["model_config"]["components"] == ["oifs"]
    assert res["model_config"]["version"] == 4



