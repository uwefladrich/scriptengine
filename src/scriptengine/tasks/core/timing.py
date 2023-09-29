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

        try:
            mode = context['se']['tasks']['timing']['mode']
        except KeyError:
            mode = False

        if mode in ('basic', 'classes', 'instances'):

            # timed function call
            start_tic = time.perf_counter()
            func_return_value = func(self, context)
            elapsed_time = time.perf_counter() - start_tic

            # logging
            if context['se']['tasks']['timing']['logging'] == 'info':
                self.log_info(f'Elapsed time: {elapsed_time:0.4f} seconds')
            elif context['se']['tasks']['timing']['logging'] == 'debug':
                self.log_debug(f'Elapsed time: {elapsed_time:0.4f} seconds')

            # update timers
            if mode in ('classes', 'instances'):
                timers = context['se']['tasks']['timing']['timers']

                class_t = timers.setdefault('classes', {})
                class_t.setdefault(self.__class__.__name__, 0)
                class_t[self.__class__.__name__] += elapsed_time

                if mode == 'instances':
                    instance_t = timers.setdefault('instances', {})
                    instance_t.setdefault(self.id, 0)
                    instance_t[self.id] += elapsed_time

            return func_return_value

        # if no timing, just return the function
        return func(self, context)

    return wrap_timed
