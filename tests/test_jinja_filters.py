from datetime import date, datetime

import pytest
import yaml

from scriptengine.context import Context as SEContext
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


@pytest.mark.parametrize("test_value", (1, 1.5, "a_string"))
def test_jinja_no_filter(test_value):
    context = SEContext(bar=test_value)
    task = from_yaml("base.context: {foo: '{{ bar }}'}")
    context += task.run(context)
    assert context["foo"] == test_value


@pytest.mark.parametrize(
    ("test_value", "format", "expected"),
    (
        ("2024/01/01", "%Y/%m/%d", date(2024, 1, 1)),
        ("2024-01-01", "%Y-%m-%d", date(2024, 1, 1)),
        ("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S", date(2024, 1, 1)),
    ),
)
def test_jinja_string_to_date(test_value, format, expected):
    context = SEContext()
    task = from_yaml(
        f"""base.context: {{foo: "{{{{ '{test_value}' | date('{format}') }}}}"}}"""
    )
    context += task.run(context)
    assert context["foo"] == expected


@pytest.mark.parametrize(
    ("test_value", "format", "expected"),
    (
        ("2024-01-01", "%Y-%m-%d", datetime(2024, 1, 1)),
        ("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S", datetime(2024, 1, 1)),
        ("2024-01-01 12:34:56", "%Y-%m-%d %H:%M:%S", datetime(2024, 1, 1, 12, 34, 56)),
    ),
)
def test_jinja_string_to_datetime(test_value, format, expected):
    context = SEContext()
    task = from_yaml(
        f"""base.context: {{foo: "{{{{ '{test_value}' | datetime('{format}') }}}}"}}"""
    )
    context += task.run(context)
    assert context["foo"] == expected


@pytest.mark.parametrize(
    ("start", "days", "hours", "minutes", "expected"),
    (
        ("2024-01-01 00:00:00", 0, 0, 0, datetime(2024, 1, 1)),
        ("2024-01-01 00:00:00", 1, 0, 0, datetime(2024, 1, 2)),
        ("2024-01-01 00:00:00", 0, 1, 0, datetime(2024, 1, 1, 1, 0)),
    ),
)
def test_jinja_filter_increment_datetime(start, days, hours, minutes, expected):
    context = SEContext()
    task = from_yaml(
        f"""
        base.context:
            foo: "{{{{ '{start}' | datetime | increment_datetime(days={days}, hours={hours}, minutes={minutes}) }}}}"
        """
    )
    context += task.run(context)
    assert context["foo"] == expected


@pytest.mark.parametrize(
    ("test_value", "expected"),
    (
        ("foo", "foo"),
        ("foo.txt", "foo.txt"),
        ("/foo.txt", "foo.txt"),
        ("/bar/foo.txt", "foo.txt"),
        ("bar/foo.txt", "foo.txt"),
        ("./foo.txt", "foo.txt"),
    ),
)
def test_jinja_filter_basetime(test_value, expected):
    context = SEContext(bar=test_value)
    task = from_yaml("base.context: {foo: '{{ bar | basename }}'}")
    context += task.run(context)
    assert context["foo"] == expected


@pytest.mark.parametrize(
    ("test_value", "expected"),
    (
        ("foo", None),
        ("foo.txt", None),
        ("/foo.txt", "/"),
        ("/bar/foo.txt", "/bar"),
        ("bar/foo.txt", "bar"),
        ("./foo.txt", "."),
    ),
)
def test_jinja_filter_dirtime(test_value, expected):
    context = SEContext(bar=test_value)
    task = from_yaml("base.context: {foo: '{{ bar | dirname }}'}")
    context += task.run(context)
    assert context["foo"] == expected


def test_jinja_filter_file_exist(tmp_path):
    context = SEContext()
    file = tmp_path / "foo.tmp"
    file.touch()
    task = from_yaml(f"""base.context: {{foo: "{{{{ '{file}' | exists }}}}"}}""")
    context += task.run(context)
    assert context["foo"] is True


def test_jinja_filter_dir_exist(tmp_path):
    context = SEContext()
    directory = tmp_path / "foo"
    directory.mkdir()
    task = from_yaml(f"""base.context: {{foo: "{{{{ '{directory}' | exists }}}}"}}""")
    context += task.run(context)
    assert context["foo"] is True


def test_jinja_filter_file_does_not_exist(tmp_path):
    context = SEContext()
    file = tmp_path / "foo.tmp"
    task = from_yaml(f"""base.context: {{foo: "{{{{ '{file}' | exists }}}}"}}""")
    context += task.run(context)
    assert context["foo"] is False


def test_jinja_filter_dir_does_not_exist(tmp_path):
    context = SEContext()
    directory = tmp_path / "foo"
    task = from_yaml(f"""base.context: {{foo: "{{{{ '{directory}' | exists }}}}"}}""")
    context += task.run(context)
    assert context["foo"] is False
