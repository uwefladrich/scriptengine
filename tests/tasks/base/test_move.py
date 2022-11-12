import os

import pytest
import yaml

from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_move_simple(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").touch()
    from_yaml(
        """
        base.move:
            src: foo
            dst: bar
        """
    ).run({})
    assert not (tmp_path / "foo").exists()
    assert (tmp_path / "bar").exists()


def test_move_dir(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").mkdir()
    (tmp_path / "foo" / "foo-1.txt").touch()
    (tmp_path / "foo" / "foo-2.txt").touch()
    from_yaml(
        """
        base.move:
            src: foo
            dst: bar
        """
    ).run({})
    assert not (tmp_path / "foo").exists()
    assert (tmp_path / "bar" / "foo-1.txt").exists()
    assert (tmp_path / "bar" / "foo-2.txt").exists()


def test_move_to_dir(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").touch()
    (tmp_path / "bar").mkdir()
    from_yaml(
        """
        base.move:
            src: foo
            dst: bar
        """
    ).run({})
    assert not (tmp_path / "foo").exists()
    assert (tmp_path / "bar" / "foo").exists()


def test_move_list(tmp_path):
    os.chdir(tmp_path)

    fnames = ("f1", "f2", "f3")
    for f in fnames:
        (tmp_path / f).touch()
    (tmp_path / "bar").mkdir()

    from_yaml(
        """
        base.move:
            src: [f1, f2, f3]
            dst: bar
        """
    ).run({})
    for f in fnames:
        assert not (tmp_path / "f1").exists()
        assert (tmp_path / "bar" / "f1").exists()


def test_move_onto_file(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "f1").touch()
    (tmp_path / "f2").touch()
    (tmp_path / "foo").mkdir()
    (tmp_path / "bar").touch()

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.move:
                src: foo
                dst: bar
            """
        ).run({})

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.move:
                src: 'f?'
                dst: bar
            """
        ).run({})

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.move:
                src: [f1, f2]
                dst: bar
            """
        ).run({})


def test_move_invalid_src(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").touch()

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.move:
                src: [[]]
                dst: foo
            """
        ).run({})


def test_move_invalid_dst(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").touch()

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.move:
                src: foo
                dst: []
            """
        ).run({})


def test_move_with_wildcard(tmp_path):
    os.chdir(tmp_path)
    foo_files = ("foo", "foobar", "foo-1", "foo-abc")
    extra_files = ("barfoo", "xyz", "Foo")
    for f in foo_files + extra_files:
        (tmp_path / f).touch()
    (tmp_path / "bar").mkdir()

    from_yaml(
        """
        base.move:
            src: foo*
            dst: bar
        """
    ).run({})

    for f in foo_files:
        assert not (tmp_path / f).exists()
        assert (tmp_path / "bar" / f).exists()
    for f in extra_files:
        assert (tmp_path / f).exists()
        assert not (tmp_path / "bar" / f).exists()


def test_move_ignore_not_found(tmp_path):
    os.chdir(tmp_path)

    from_yaml(
        """
        base.move:
            src: foo
            dst: bar
            ignore_not_found: true
        """
    ).run({})

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.move:
                src: foo
                dst: bar
            """
        ).run({})
