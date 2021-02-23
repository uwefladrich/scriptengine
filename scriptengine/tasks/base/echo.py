"""Echo task for ScriptEngine."""

from scriptengine.tasks.core import Task, timed_runner
from scriptengine.helpers import terminal_colors as tc


class Echo(Task):
    """Echo task, writes a (coloured) message to stdout
    """

    _required_arguments = ('msg', )

    def __init__(self, arguments):
        Echo.check_arguments(arguments)
        super().__init__(arguments)

    def __str__(self):
        return f'Echo: {getattr(self, "msg", "")}'

    @timed_runner
    def run(self, context):

        log_msg = self.msg.replace('\n', '')
        self.log_info(log_msg[:15]+'...' if len(log_msg) > 18 else log_msg)

        msg = self.getarg('msg', context)
        print(tc.LIGHTBLUE + str(msg) + tc.RESET)
