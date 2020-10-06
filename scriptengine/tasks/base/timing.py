"""ScriptEngine timing for tasks: provides timing of Task classes .run() method
"""

import time
import functools


def timed_runner(func):
    """Wrapper for run() functions of SE tasks. To be used as decorator as follows:

        from scriptengine.task_timing import timed_runner
        class Foo(Task):
            # ...
            @timed_runner
            def run(self, context):
                # ...
    """

    @functools.wraps(func)
    def wrap_timed(self, context):

        timing = context.get(context.get('_se_task_timing', object()))
        if timing:

            mode = timing.get('mode')
            if mode in ('basic', 'classes', 'instances'):

                tic = time.perf_counter()
                value = func(self, context)
                elapsed_time = time.perf_counter() - tic

                logging = timing.get('logging')
                if logging == 'info':
                    self.log_info(
                        f'Elapsed time: {elapsed_time:0.4f} seconds')
                if logging == 'debug':
                    self.log_debug(
                        f'Elapsed time: {elapsed_time:0.4f} seconds')

                if mode in ('classes', 'instances'):
                    timers = timing.setdefault('classes', {})
                    my_name = self.__class__.__name__
                    timers.setdefault(my_name, 0)
                    timers[my_name] += elapsed_time

                    if mode == 'instances':
                        timers = timing.setdefault('instances', {})
                        timers.setdefault(self.id, 0)
                        timers[self.id] += elapsed_time

                return value

        # Default return if no timing
        return func(self, context)

    return wrap_timed
