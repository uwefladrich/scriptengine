import os

import yaml

from scriptengine.engines import SimpleScriptEngine
from scriptengine.yaml.parser import parse


def _from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def tests_setenv():
    t = _from_yaml(
        """
        base.setenv:
            FOO: foo
        """
    )
    t.run({})
    assert os.environ["FOO"] == "foo"


def test_getenv():
    os.environ["FOO"] = "foo"

    t = _from_yaml(
        """
        base.getenv:
            foo: FOO
        """
    )
    ctxt = {}
    ctxt_upd = t.run(ctxt)
    ctxt += ctxt_upd
    assert ctxt["foo"] == "foo"


def test_getenv_not_exists():
    t = _from_yaml(
        """
        base.getenv:
            bar: BAR
        """
    )
    ctxt = {}
    ctxt_upd = t.run(ctxt)
    ctxt += ctxt_upd
    assert "bar" not in ctxt
