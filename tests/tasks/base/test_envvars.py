import logging
import os

import yaml

from scriptengine.context import Context
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
    t.run(Context())
    assert os.environ["FOO"] == "foo"


def test_getenv():
    os.environ["FOO"] = "foo"

    t = _from_yaml(
        """
        base.getenv:
            foo: FOO
        """
    )
    ctxt = t.run(Context())
    assert ctxt["foo"] == "foo"


def test_getenv_not_exists():
    t = _from_yaml(
        """
        base.getenv:
            bar: BAR
        """
    )
    ctxt = t.run(Context())
    assert "bar" not in ctxt


def test_unsetenv_one_var():
    os.environ["FOO"] = "foo"

    t = _from_yaml(
        """
        base.unsetenv:
            vars: FOO
        """
    )
    t.run(Context())
    assert "FOO" not in os.environ
    assert "BAR" not in os.environ


def test_unsetenv_two_vars():
    os.environ["FOO"] = "foo"
    os.environ["BAR"] = "1"

    t = _from_yaml(
        """
        base.unsetenv:
            vars:
                - FOO
                - BAR
        """
    )
    t.run(Context())
    assert "FOO" not in os.environ
    assert "BAR" not in os.environ


def test_unsetenv_not_exists(caplog):
    t = _from_yaml(
        """
        base.unsetenv:
            vars: FOO
        """
    )
    with caplog.at_level(logging.WARN, logger="se.task"):
        t.run(Context())
        assert "Environment variable 'FOO' does not exist" in [
            rec.message for rec in caplog.records
        ]
