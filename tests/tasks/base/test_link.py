import logging
import os

import pytest
import yaml

from scriptengine.exceptions import (
    ScriptEngineTaskArgumentMissingError,
    ScriptEngineTaskRunError,
)
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_link_simple(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").touch()
    from_yaml(
        """
        base.link:
            target: foo
            link: bar
        """
    ).run({})
    assert (tmp_path / "bar").is_file()


def test_link_to_dir(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").touch()
    (tmp_path / "bar").mkdir()
    from_yaml(
        f"""
        base.link:
            target: {tmp_path / 'foo'}
            link: bar
        """
    ).run({})
    assert (tmp_path / "bar" / "foo").is_file()


def test_link_to_default_dir(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "foo").mkdir()
    (tmp_path / "foo" / "bar").touch()
    from_yaml(
        """
        base.link:
            target: foo/bar
        """
    ).run({})
    assert (tmp_path / "bar").is_file()


def test_link_wildcards(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "f1").touch()
    (tmp_path / "f2").touch()
    (tmp_path / "bar").mkdir()
    from_yaml(
        f"""
        base.link:
            target: {tmp_path / 'f?'}
            link: bar
        """
    ).run({})
    assert (tmp_path / "bar" / "f1").is_file()
    assert (tmp_path / "bar" / "f2").is_file()


def test_link_list(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "f1").touch()
    (tmp_path / "f2").touch()
    (tmp_path / "bar").mkdir()
    from_yaml(
        f"""
        base.link:
            target:
                - {tmp_path / 'f1'}
                - {tmp_path / 'f2'}
            link: bar
        """
    ).run({})
    assert (tmp_path / "bar" / "f1").is_file()
    assert (tmp_path / "bar" / "f2").is_file()


def test_link_multiple_targets_to_file(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "f1").touch()
    (tmp_path / "f2").touch()
    (tmp_path / "bar").touch()

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.link:
                target: [f1, f2]
                link: bar
            """
        ).run({})


def test_link_multiple_link_names(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "bar").touch()

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.link:
                target: bar
                link: [f1, f2]
            """
        ).run({})


def test_link_missing_target(tmp_path):
    os.chdir(tmp_path)

    with pytest.raises(ScriptEngineTaskArgumentMissingError):
        from_yaml(
            """
            base.link:
                link: foo
            """
        ).run({})


def test_link_invalid_target(tmp_path):
    os.chdir(tmp_path)

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.link:
                target: [[]]
                link: foo
            """
        ).run({})


def test_link_empty_target(tmp_path, caplog):
    os.chdir(tmp_path)

    with caplog.at_level(logging.WARNING, logger="se.task"):
        from_yaml(
            """
            base.link:
                target: foo*
                link: bar
            """
        ).run({})
    assert "No valid targets" in caplog.text


def test_link_simple_legacy(tmp_path, caplog):
    os.chdir(tmp_path)
    (tmp_path / "foo").touch()
    with caplog.at_level(logging.WARNING, logger="se.task"):
        from_yaml(
            """
            base.link:
                src: foo
                dst: bar
            """
        ).run({})
    assert "argument is deprecated" in caplog.text
    assert (tmp_path / "bar").is_file()
