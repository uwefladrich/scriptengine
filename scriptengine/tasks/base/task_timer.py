"""TaskTimer for ScriptEngine."""

from scriptengine.tasks.base import Task


class TaskTimer(Task):
    """TaskTimer, controls ScriptEngine task timing feature

       Arguments:
         mode (required):   one of
                            False:       Timing is switched off.
                            'basic':     Each task is timed, log messages are
                                         written according to 'logging'
                                         argument.
                            'classes':   As for 'basic', plus times are
                                         accumulated for task classes.
                            'instances': As for 'classes', plus times are
                                         accumulated for each individual task
                                         instance.
        set (optional):     The context key used to store timing information.
                            This argument is needed if 'mode' is not False.
        logging (optional): one of
                            False:   No time logging after each task. Does not
                                     affect statistic collection.
                            'info':  Logging to the info logger.
                            'debug': Logging to the debug logger.
    """
    _required_arguments = ('mode', )

    def __init__(self, arguments):
        TaskTimer.check_arguments(arguments)
        super().__init__(arguments)

    def run(self, context):

        mode = self.getarg('mode', context)
        self.log_info(f'Setting timer mode to "{mode}"')
        if mode not in (False, 'basic', 'classes', 'instances'):
            raise RuntimeError('Unknown mode in TaskTimer: must be one of '
                               '"off", "basic", "classes", "instances", '
                               f'not "{mode}"')

        if mode:
            timer_key = self.getarg('set', context, default=None)
            try:
                timer_context = context.setdefault(timer_key, {})
            except TypeError:
                raise RuntimeError('Invalid context key in "set" argument of '
                                   f'TaskTimer: {timer_key}"')

            self.log_debug(f'Using timer key "{timer_key}"')

            timer_context['mode'] = mode

            logging = self.getarg('logging', context, default=False)
            if logging not in (False, 'info', 'debug'):
                raise RuntimeError(
                        'Unknown logging mode in TaskTimer: must be one of '
                        f'"off", "info", "debug", not "{logging}"')
            timer_context['logging'] = logging

            context['_se_task_timing'] = timer_key

        else:
            context['_se_task_timing'] = False
