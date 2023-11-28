import pytest
import yaml

from scriptengine.jobs import Job
from scriptengine.tasks.base.echo import Echo
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_create():
    assert type(Job()) is Job


def test_create_invalid_todo():
    with pytest.raises(ValueError):
        Job([1, 2, 3])


def test_create_from_yaml():
    j = from_yaml(
        """
        do:
            - base.echo:
                msg: Hello!
    """
    )
    assert type(j) is Job
    assert type(j.todo[0]) is Echo
