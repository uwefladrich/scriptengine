import yaml

from scriptengine.engines import SimpleScriptEngine
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_context_update_in_job(capsys):
    s = from_yaml(
        """
        - do:
            - base.context:
                foo: 1
            - base.echo:
                msg: "foo is '{{foo}}'"
        """
    )
    SimpleScriptEngine().run(s, context={})
    captured = capsys.readouterr()
    assert "foo is '1'" in captured.out


def test_echo_updates_context_in_job(capsys):
    s = from_yaml(
        """
        - do:
            - base.command:
                name: echo
                args: [-n, Hello, world!]
                stdout: message
            - base.echo:
                msg: "{{message}}"
        """
    )
    SimpleScriptEngine().run(s, context={})
    captured = capsys.readouterr()
    assert "Hello world!" in captured.out
