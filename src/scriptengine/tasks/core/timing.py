"""ScriptEngine timing for tasks: provides timing of Task classes .run() method
"""

import copy
import functools
import time

from scriptengine.context import Context


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

        mode = context.get("se.tasks.timing.mode")

        if mode in ("basic", "classes", "instances"):

            # timed function call
            start_tic = time.perf_counter()
            context_update = func(self, context) or Context()
            elapsed_time = time.perf_counter() - start_tic

            # logging
            if context["se.tasks.timing.logging"] == "info":
                self.log_info(f"Elapsed time: {elapsed_time:0.4f} seconds")
            elif context["se.tasks.timing.logging"] == "debug":
                self.log_debug(f"Elapsed time: {elapsed_time:0.4f} seconds")

            # update timers
            if mode in ("classes", "instances"):
                timers = copy.deepcopy(context["se.tasks.timing.timers"])

                class_t = timers.setdefault("classes", {})
                class_t.setdefault(self.__class__.__name__, 0)
                class_t[self.__class__.__name__] += elapsed_time

                if mode == "instances":
                    instance_t = timers.setdefault("instances", {})
                    instance_t.setdefault(self.id, 0)
                    instance_t[self.id] += elapsed_time

                timer_update = Context()
                timer_update["se.tasks.timing.timers"] = timers

                context_update += timer_update

            return context_update

        # if no timing, just return the function
        return func(self, context)

    return wrap_timed
