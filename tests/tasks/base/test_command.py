import logging
import os

import yaml

import scriptengine.logging
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.SafeLoader))


def test_command_ls(tmp_path, caplog):

    os.chdir(tmp_path)
    (tmp_path / "foo").touch()

    caplog.clear()
    scriptengine.logging.configure(logging.INFO)
    logger = logging.getLogger("se.task")
    logger.propagate = True

    from_yaml(
        """
        base.command:
          name: ls
          args: [ foo ]
        """
    ).run({})
    assert ("se.task", logging.INFO, "foo") in caplog.record_tuples


def test_command_ls_not_exists(tmp_path, caplog):

    os.chdir(tmp_path)

    caplog.clear()
    scriptengine.logging.configure(logging.INFO)
    logger = logging.getLogger("se.task")
    logger.propagate = True

    from_yaml(
        """
        base.command:
          name: ls
          args: [ bar ]
          ignore_error: true
        """
    ).run({})
    assert "Command returned error code " in caplog.text
