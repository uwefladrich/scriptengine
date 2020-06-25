"""ScriptEngine timing for tasks: provides timing of Task classes .run() method
"""

import time
import functools


TIMING_CONTEXT_KEY = "se_timing"


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

        mode = context.get(TIMING_CONTEXT_KEY, {}).get("mode", None)

        if mode in ("basic", "classes", "instances"):

            tic = time.perf_counter()
            value = func(self, context)
            elapsed_time = time.perf_counter() - tic

            self.log_info(f"Elapsed time: {elapsed_time:0.4f} seconds")

            if mode in ("classes", "instances"):
                timers = context[TIMING_CONTEXT_KEY].setdefault("timers", {}).setdefault("classes", {})
                my_name = self.__class__.__name__
                timers.setdefault(my_name, 0)
                timers[my_name] += elapsed_time

                if mode == "instances":
                    timers = context[TIMING_CONTEXT_KEY].setdefault("timers", {}).setdefault("instances", {})
                    timers.setdefault(self.id, 0)
                    timers[self.id] += elapsed_time

            return value

        # Default return if no timing
        return func(self, context)

    return wrap_timed
