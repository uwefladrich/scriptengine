from se.tasks import Task
from se.helpers import render_string_recursive

from se.helpers import TerminalColors as tc

class Echo(Task):

    def __init__(self, dict):
        super(Echo, self).__init__(dict, 'msg')

    def __str__(self):
        return 'Echo: {}'.format(self.msg)

    def run(self, *, dryrun=False, **config):
        if dryrun:
            print(render_string_recursive(str(self), **config))
        else:
            print((tc.GREEN+tc.BOLD+tc.DIM + 'ScriptEngineEcho:' + tc.RESET
                   + tc.GREEN+tc.BOLD + ' {}'
                   + tc.RESET).format(render_string_recursive(self.msg, **config)))
        return None
