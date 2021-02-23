import pytest

from time import sleep
from attrdict import AttrDict

from scriptengine.tasks import Task, timed_runner
from scriptengine.tasks.base.task_timer import TaskTimer
from scriptengine.exceptions import ScriptEngineTaskArgumentMissingError


class WaitASecond(Task):
    @timed_runner
    def run(self, context):
        sleep(1.0)


def test_create_task_timing():
    tests = (
        {'mode': False},
        {'mode': 'basic'},
        {'mode': 'basic', 'logging': False},
        {'mode': 'basic', 'logging': 'info'},
        {'mode': 'basic', 'logging': 'debug'},
        {'mode': 'classes'},
        {'mode': 'instances'},
    )
    for t in tests:
        assert type(TaskTimer(t)) == TaskTimer


def test_create_task_timing_with_missing_argument():
    with pytest.raises(ScriptEngineTaskArgumentMissingError):
        TaskTimer({})


def test_task_timing():
    timer_mode = 'instances'
    timer_logging = False

    timer = TaskTimer({'mode': timer_mode,
                       'logging': timer_logging})
    timed = WaitASecond()

    context = AttrDict(
        {
            'se': {
                'tasks': {
                    'timing': {
                        'mode': False,
                        'logging': None,
                        'timers': {},
                    }
                }
            }
        }
    )
    timer.run(context)
    timed.run(context)

    assert context.se.tasks.timing.mode == timer_mode
    assert context.se.tasks.timing.logging == timer_logging

    assert context.se.tasks.timing.timers.classes[timed.__class__.__name__] > 1.0
    assert context.se.tasks.timing.timers.instances[timed.id] > 1.0
