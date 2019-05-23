from se.tasks import Task
from se.helpers import render_string_recursive

from se.helpers import TerminalColors as tc


class Echo(Task):

    def __init__(self, dict):
        super(Echo, self).__init__(__name__, dict, 'msg')
        self.log.debug('Creating "{}"'.format(self.msg))

    def __str__(self):
        return 'Echo: {}'.format(self.msg)

    def run(self, *, dryrun=False, **config):
        self.log.info('{}'.format(render_string_recursive(self.msg, **config)))
        if dryrun:
            print(render_string_recursive(str(self), **config))
        else:
            print((tc.LIGHTBLUE+'{}'+tc.RESET).format(render_string_recursive(self.msg, **config)))
        return None
