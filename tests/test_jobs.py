import yaml
from deepdiff import Delta

from scriptengine.jobs import Job
from scriptengine.tasks.base.echo import Echo
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_job_create():
    assert type(Job()) is Job


def test_job_create_from_yaml():
    j = from_yaml(
        """
        do:
            - base.echo:
                msg: Hello!
    """
    )
    assert type(j) is Job
    assert type(j.todo[0]) is Echo


def test_job_simple_run(capsys):
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


def test_job_simple_loop(capsys):
    j = from_yaml(
        """
        base.echo:
            msg: 'Hello {{item}}'
        loop: [1, 2, 3]
    """
    )
    j.run({})
    captured = capsys.readouterr()
    assert "Hello 1" in captured.out
    assert "Hello 2" in captured.out
    assert "Hello 3" in captured.out


def test_job_loop_in(capsys):
    j = from_yaml(
        """
        base.echo:
            msg: 'Hello {{item}}'
        loop:
            in: [1, 2, 3]
    """
    )
    j.run({})
    captured = capsys.readouterr()
    assert "Hello 1" in captured.out
    assert "Hello 2" in captured.out
    assert "Hello 3" in captured.out


def test_job_loop_with_in(capsys):
    j = from_yaml(
        """
        base.echo:
            msg: 'Hello {{foo}}'
        loop:
            with: foo
            in: [1, 2, 3]
    """
    )
    j.run({})
    captured = capsys.readouterr()
    assert "Hello 1" in captured.out
    assert "Hello 2" in captured.out
    assert "Hello 3" in captured.out


def test_job_loop_from_context(capsys):
    j = from_yaml(
        """
        base.echo:
            msg: 'Hello {{item}}'
        loop: '[1, 2, 3]'
    """
    )
    j.run({})
    captured = capsys.readouterr()
    assert "Hello 1" in captured.out
    assert "Hello 2" in captured.out
    assert "Hello 3" in captured.out


def test_job_loop_in_dict(capsys):
    j = from_yaml(
        """
        base.echo:
            msg: '{{key}} is {{value}}'
        loop:
            in:
                foo: 1
                bar: 2
                baz: 3
    """
    )
    j.run({})
    captured = capsys.readouterr()
    assert "foo is 1" in captured.out
    assert "bar is 2" in captured.out
    assert "baz is 3" in captured.out


def test_job_loop_with_in_dict(capsys):
    j = from_yaml(
        """
        base.echo:
            msg: '{{one}} is {{two}}'
        loop:
            with: ['one', 'two']
            in:
                foo: 1
                bar: 2
                baz: 3
    """
    )
    j.run({})
    captured = capsys.readouterr()
    assert "foo is 1" in captured.out
    assert "bar is 2" in captured.out
    assert "baz is 3" in captured.out


def test_job_when_true(capsys):
    j = from_yaml("""
        base.echo:
            msg: Hello, world!
        when: 'true'
    """)
    j.run({})
    captured = capsys.readouterr()
    assert 'Hello, world!' in captured.out


def test_job_when_false(capsys):
    j = from_yaml("""
        base.echo:
            msg: Hello, world!
        when: 'false'
    """)
    j.run({})
    captured = capsys.readouterr()
    assert 'Hello, world!' not in captured.out


def test_job_returns_delta():
    j = from_yaml(
        """
        do:
            - base.context:
                foo: 1
    """
    )
    assert type(j.run({})) is Delta


def test_job_updates_dict_simple():
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


def test_job_updates_dict_nested():
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


def test_job_adds_to_list():
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
