from se.tasks import Task
from se.helpers import render_string

from se.helpers import TerminalColors as tc


class Echo(Task):

    def __init__(self, dict):
        super(Echo, self).__init__(__name__, dict, 'msg')
        self.log_debug('Creating "{}"'.format(self.msg))

    def __str__(self):
        return 'Echo: {}'.format(self.msg)

    def run(self, *, dryrun=False, **config):
        self.log_info('{}'.format(render_string(self.msg, **config)))
        if dryrun:
            print(render_string(str(self), **config))
        else:
            print((tc.LIGHTBLUE+'{}'+tc.RESET).format(render_string(self.msg, **config)))
        return None
