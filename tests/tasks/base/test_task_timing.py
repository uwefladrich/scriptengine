from time import sleep

import pytest
import yaml

from scriptengine.context import Context
from scriptengine.exceptions import ScriptEngineTaskArgumentMissingError
from scriptengine.tasks.base.echo import Echo
from scriptengine.tasks.base.task_timer import TaskTimer
from scriptengine.tasks.core import Task, timed_runner
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


class WaitASecond(Task):
    @timed_runner
    def run(self, context):
        sleep(1.0)


def test_create_task_timing():
    tests = (
        {"mode": False},
        {"mode": "basic"},
        {"mode": "basic", "logging": False},
        {"mode": "basic", "logging": "info"},
        {"mode": "basic", "logging": "debug"},
        {"mode": "classes"},
        {"mode": "instances"},
    )
    for t in tests:
        assert type(TaskTimer(t)) == TaskTimer


def test_create_task_timing_with_missing_argument():
    with pytest.raises(ScriptEngineTaskArgumentMissingError):
        TaskTimer({})


def test_task_timing():
    timer_mode = "instances"
    timer_logging = False

    timer = TaskTimer({"mode": timer_mode, "logging": timer_logging})
    timed = WaitASecond()

    context = Context(
        {
            "se.tasks.timing": {
                "mode": False,
                "logging": None,
                "timers": {},
            }
        }
    )

    context += timer.run(context)
    context += timed.run(context)

    assert context["se.tasks.timing"]["mode"] == timer_mode
    assert context["se.tasks.timing"]["logging"] == timer_logging

    assert context["se.tasks.timing.timers.classes"][timed.__class__.__name__] > 1.0
    assert context["se.tasks.timing.timers.instances"][timed.id] > 1.0


def test_task_timer_after_echo():

    context = Context(
        {
            "se.tasks.timing": {
                "mode": False,
                "logging": None,
                "timers": {},
            }
        }
    )
    context += TaskTimer({"mode": "classes"}).run(context)
    context += Echo({"msg": "Hello!"}).run(context)

    assert "se.tasks.timing.timers.classes" in context
    assert context["se.tasks.timing.timers.classes.Echo"] > 0.0


def test_task_timer_in_job():

    context = Context(
        {
            "se.tasks.timing": {
                "mode": False,
                "logging": None,
                "timers": {},
            }
        }
    )
    context += TaskTimer({"mode": "classes"}).run(context)

    job = from_yaml(
        """
        do:
            - base.echo:
                msg: Hello
        """
    )
    context += job.run(context)

    assert "se.tasks.timing.timers.classes" in context
    assert context["se.tasks.timing.timers.classes.Echo"] > 0.0
