import yaml

from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_simple_run(capsys):
    msg1 = "Hello, world!"
    msg2 = "Hello, Mars!"
    j = from_yaml(
        f"""
        do:
            - base.echo:
                msg: {msg1}
            - base.echo:
                msg: {msg2}
    """
    )
    j.run({})
    captured = capsys.readouterr()
    assert msg1 in captured.out
    assert msg2 in captured.out


def test_updates_dict_simple():
    j = from_yaml(
        """
        do:
            - base.context:
                foo: 1
    """
    )
    c = {} + j.run({})
    assert "foo" in c
    assert c["foo"] == 1


def test_updates_dict_nested():
    j = from_yaml(
        """
        do:
            - base.context:
                foo:
                    a: 1
                    b: 2
            - base.context:
                foo:
                    c: 3
    """
    )
    c = {} + j.run({})
    assert c["foo"]["a"] == 1
    assert c["foo"]["b"] == 2
    assert c["foo"]["c"] == 3


def test_adds_to_list():
    j = from_yaml(
        """
        do:
            - base.context:
                foo:
                    - 1
                    - 2
            - base.context:
                foo:
                    - 3
    """
    )
    c = {} + j.run({})
    assert c["foo"] == [1, 2, 3]
