import pytest

from time import sleep

from scriptengine.tasks.base import Task, \
                                    TaskTimer
from scriptengine.exceptions import ScriptEngineTaskArgumentMissingError
from scriptengine.tasks.base.timing import timed_runner


class WaitASecond(Task):
    @timed_runner
    def run(self, context):
        sleep(1.0)


def test_create_task_timing():
    tests = (
        {'mode': False},
        {'mode': 'basic', 'set': 'foo'},
        {'mode': 'basic', 'set': 'foo', 'logging': False},
        {'mode': 'basic', 'set': 'foo', 'logging': 'info'},
        {'mode': 'basic', 'set': 'foo', 'logging': 'debug'},
        {'mode': 'classes', 'set': 'foo'},
        {'mode': 'instances', 'set': 'foo'},
    )
    for t in tests:
        assert type(TaskTimer(t)) == TaskTimer


def test_create_task_timing_with_missing_argument():
    with pytest.raises(ScriptEngineTaskArgumentMissingError):
        TaskTimer({})


def test_task_timing():
    timer_mode = 'instances'
    timer_set = 'foo'
    timer_logging = False

    timer = TaskTimer({'mode': timer_mode,
                       'set': timer_set,
                       'logging': timer_logging})
    timed = WaitASecond()

    context = {}
    timer.run(context)
    timed.run(context)

    assert context['_se_task_timing'] == timer_set
    assert timer_set in context
    assert context[timer_set]['mode'] == timer_mode
    assert context[timer_set]['logging'] == timer_logging

    assert context[timer_set]['classes'][timed.__class__.__name__] > 1.0
    assert context[timer_set]['instances'][timed.id] > 1.0
