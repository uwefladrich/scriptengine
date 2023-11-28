import logging
import os
import time

import yaml

from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.SafeLoader))


def test_command_ls(tmp_path):
    os.chdir(tmp_path)
    f = tmp_path / "foo"
    f.touch()
    time.sleep(2)

    t = from_yaml(
        f"""
        base.command:
          name: ls
          args: [ {f.name} ]
          stdout: ls_stdout
        """
    )

    c = t.run({})
    assert "foo" in c["ls_stdout"]

    f.unlink()


def test_command_ls_not_exists(tmp_path, caplog):
    os.chdir(tmp_path)

    t = from_yaml(
        """
        base.command:
          name: ls
          args: [ foo ]
          ignore_error: true
          stderr: ls_stderr
        """
    )

    with caplog.at_level(logging.WARN, logger="se.task"):
        c = t.run({})
        assert "Command returned error code 2" in [
            rec.message for rec in caplog.records
        ]
        assert len(c["ls_stderr"]) > 1
