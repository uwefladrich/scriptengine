import yaml

from scriptengine.engines import SimpleScriptEngine
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_when_true(capsys):
    j = from_yaml(
        """
        base.echo:
            msg: Hello, world!
        when: 'true'
    """
    )
    j.run({})
    captured = capsys.readouterr()
    assert "Hello, world!" in captured.out


def test_when_false(capsys):
    j = from_yaml(
        """
        base.echo:
            msg: Hello, world!
        when: 'false'
    """
    )
    j.run({})
    captured = capsys.readouterr()
    assert "Hello, world!" not in captured.out


def test_when_clause_parses_noparse_parameter(capsys):
    s = from_yaml(
        """
        - base.context:
            foo: me
            bar: !noparse_jinja "{{ foo }}"
        - when: "{{ bar|render == 'me' }}"
          base.echo:
            msg: Hello!
        """
    )
    SimpleScriptEngine().run(s, context={})
    captured = capsys.readouterr()
    assert "Hello!" in captured.out
