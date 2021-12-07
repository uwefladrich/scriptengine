import yaml

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
