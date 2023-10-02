from pathlib import Path
import pytest

import yaml

from scriptengine.context import Context
from scriptengine.yaml.parser import parse
from scriptengine.engines import SimpleScriptEngine
from scriptengine.exceptions import ScriptEngineTaskRunError


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_simple_include(tmp_path):
    f = Path(tmp_path / "include.yml")
    f.write_text(
        """
        base.context:
          foo: 1
        """
    )
    t = from_yaml(
        """
        base.include:
          src: include.yml
        """
    )
    c = t.run(
        Context(
            {
                "se.cli.cwd": str(tmp_path),
                "se.cli.script_path": str(tmp_path),
                "se.instance": SimpleScriptEngine(),
            }
        )
    )
    assert "foo" in c and c["foo"] == 1


def test_include_ignore_not_found_works(tmp_path):
    t = from_yaml(
        """
        base.include:
          src: include.yml
          ignore_not_found: true
        """
    )
    t.run(
        Context(
            {
                "se.cli.cwd": str(tmp_path),
                "se.cli.script_path": str(tmp_path),
                "se.instance": SimpleScriptEngine(),
            }
        )
    )


def test_include_not_found_raises_error(tmp_path):
    t = from_yaml(
        """
        base.include:
          src: include.yml
        """
    )
    with pytest.raises(ScriptEngineTaskRunError):
        t.run(
            Context(
                {
                    "se.cli.cwd": str(tmp_path),
                    "se.cli.script_path": str(tmp_path),
                    "se.instance": SimpleScriptEngine(),
                }
            )
        )
