import yaml

from scriptengine.engines import SimpleScriptEngine
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_context_add_to_list(capsys):
    s = from_yaml(
        """
        - base.context:
            foo.bar: [1]
        - base.context:
            foo.bar: [2]
        - base.echo:
            msg: "foo.bar is {{ foo.bar }}"
        """
    )
    SimpleScriptEngine().run(s, context={})
    captured = capsys.readouterr()
    assert "foo.bar is [1, 2]" in captured.out
