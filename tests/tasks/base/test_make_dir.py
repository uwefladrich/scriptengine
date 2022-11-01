import os

import pytest
import yaml

from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_make_dir_simple(tmp_path):
    os.chdir(tmp_path)

    from_yaml(
        """
        base.make_dir:
            path: foo
        """
    ).run({})

    assert (tmp_path / "foo").is_dir()


def test_make_dir_list(tmp_path):
    os.chdir(tmp_path)

    from_yaml(
        """
        base.make_dir:
            path: [f1, f2, f3]
        """
    ).run({})

    assert (tmp_path / "f1").is_dir()
    assert (tmp_path / "f2").is_dir()
    assert (tmp_path / "f3").is_dir()


def test_make_dir_exists(tmp_path):
    os.chdir(tmp_path)

    (tmp_path / "foo").mkdir()
    (tmp_path / "bar").touch()

    from_yaml(
        """
        base.make_dir:
            path: foo
        """
    ).run({})

    with pytest.raises(ScriptEngineTaskRunError):
        from_yaml(
            """
            base.make_dir:
                path: bar
            """
        ).run({})
