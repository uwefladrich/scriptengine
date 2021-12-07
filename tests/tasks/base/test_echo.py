import pytest

from scriptengine.exceptions import ScriptEngineTaskArgumentMissingError
from scriptengine.tasks.base.echo import Echo


def test_create_echo():
    assert type(Echo({"msg": "hello"})) is Echo


def test_create_echo_without_msg():
    with pytest.raises(ScriptEngineTaskArgumentMissingError):
        Echo({})


def test_echo_output(capsys):
    message = "Hello, world"
    Echo({"msg": message}).run({})
    captured = capsys.readouterr()
    assert message in captured.out
