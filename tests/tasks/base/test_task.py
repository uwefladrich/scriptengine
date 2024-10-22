import pytest

from scriptengine.exceptions import (
    ScriptEngineTaskArgumentInvalidError,
    ScriptEngineTaskArgumentMissingError,
)
from scriptengine.tasks.core import Task


def test_create_task():
    assert isinstance(Task(), Task)


def test_create_task_with_args():
    assert isinstance(Task({"foo": 1, "bar": 2}), Task)


def test_create_task_with_invalid_args():
    tests = (
        (Task, {"run": 1}),
        (Task, {"id": 2}),
        (Task, {"run": 1, "id": 2}),
    )

    for task_class, parameters in tests:
        with pytest.raises(ScriptEngineTaskArgumentInvalidError):
            task_class(parameters)


def test_create_task_with_missing_args():
    with pytest.raises(ScriptEngineTaskArgumentMissingError):
        Task().getarg("foo")
