import logging
import os
import time

import yaml

from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.SafeLoader))


def test_command_ls(tmp_path, caplog):
    os.chdir(tmp_path)
    (tmp_path / "foo").touch()
    time.sleep(2)

    t = from_yaml(
        """
        base.command:
          name: ls
          args: [ foo ]
        """
    )

    with caplog.at_level(logging.INFO, logger="se.task"):
        t.run({})
        assert "foo" in [rec.message for rec in caplog.records]


def test_command_ls_not_exists(tmp_path, caplog):
    os.chdir(tmp_path)

    t = from_yaml(
        """
        base.command:
          name: ls
          args: [ foo ]
          ignore_error: true
        """
    )

    with caplog.at_level(logging.WARN, logger="se.task"):
        t.run({})
        assert "Command returned error code 2" in [
            rec.message for rec in caplog.records
        ]
