"""TaskTimer for ScriptEngine."""

from scriptengine.tasks.core import Task
from scriptengine.exceptions import ScriptEngineTaskRunError


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
        if mode not in (False, 'basic', 'classes', 'instances'):
            msg = ('Unknown mode in TaskTimer: must be one of "off", "basic", '
                   f'"classes", "instances", not "{mode}"')
            self.log_error(msg)
            raise ScriptEngineTaskRunError(msg)

        if mode:
            logging = self.getarg('logging', context, default=False)
            if logging not in (False, 'info', 'debug'):
                msg = ('Unknown logging mode in TaskTimer: must be one of '
                       f'"off", "info", "debug", not "{logging}"')
                self.log_error(msg)
                raise ScriptEngineTaskRunError(msg)
            self.log_info(f'Task timing activated in mode "{mode}" and '
                          f'logging to "{logging}"')
        else:
            logging = False
            self.log_info('Task timing is switched off')

        context['se']['tasks']['timing']['mode'] = mode
        context['se']['tasks']['timing']['logging'] = logging
