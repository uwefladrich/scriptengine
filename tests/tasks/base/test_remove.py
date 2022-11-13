import logging
import os

import pytest
import yaml

from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_remove_file_simple(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").touch()
    from_yaml(
        """
        base.remove:
            path: foo
        """
    ).run({})
    assert not (tmp_path / "foo").exists()


def test_remove_dir_simple(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").mkdir()
    (tmp_path / "foo" / "bar").touch()
    from_yaml(
        """
        base.remove:
            path: foo
        """
    ).run({})
    assert not (tmp_path / "foo").exists()


def test_remove_list(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").mkdir()
    (tmp_path / "foo" / "bar").touch()
    (tmp_path / "bar").touch()
    from_yaml(
        """
        base.remove:
            path: [foo, bar]
        """
    ).run({})
    assert not (tmp_path / "foo").exists()
    assert not (tmp_path / "bar").exists()


def test_remove_invalid_path(tmp_path):
    os.chdir(tmp_path)

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.remove:
                path: [[]]
            """
        ).run({})


def test_remove_with_wildcard(tmp_path):
    os.chdir(tmp_path)
    foo_files = ("foo", "foobar", "foo-1", "foo-abc")
    extra_files = ("barfoo", "xyz", "Foo")
    for f in foo_files + extra_files:
        (tmp_path / f).touch()

    from_yaml(
        """
        base.remove:
            path: foo*
        """
    ).run({})

    for f in foo_files:
        assert not (tmp_path / f).exists()
    for f in extra_files:
        assert (tmp_path / f).exists()


def test_remove_ignore_not_found(tmp_path, caplog):
    os.chdir(tmp_path)

    from_yaml(
        """
        base.remove:
            path: foo
            ignore_not_found: true
        """
    ).run({})

    #   with pytest.raises(ScriptEngineTaskRunError):
    #       from_yaml(
    #           """
    #           base.remove:
    #               path: foo
    #           """
    #       ).run({})

    with caplog.at_level(logging.WARNING, logger="se.task"):
        from_yaml(
            """
            base.remove:
                path: foo
            """
        ).run({})

    assert "Deprecation warning! base.remove has not found anything" in caplog.text


def test_remove_permission_denied(tmp_path):
    os.chdir(tmp_path)

    foo = tmp_path / "foo"
    foo.mkdir()
    (foo / "bar").touch()
    foo.chmod(mode=0o550)

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.remove:
                path: foo
            """
        ).run({})
    assert foo.exists()

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.remove:
                path: foo/bar
            """
        ).run({})
    assert foo.exists()

    foo.chmod(mode=0o660)
