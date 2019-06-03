import shutil

from se.tasks import Task
from se.helpers import render_string

class Copy(Task):

    def __init__(self, dict):
        super(Copy, self).__init__(__name__, dict, 'src', 'dst')
        self.log_debug('Creating "{}"'.format(dict))

    def __str__(self):
        return 'Copy: {} --> {}'.format(self.src, self.dst)

    def run(self, *, dryrun=False, **config):
        self.log_info('{} --> {}'.format(render_string(self.src, **config),
                                         render_string(self.dst, **config)))
        if dryrun:
            print(render_string(str(self), **config))
        else:
            shutil.copy(render_string(self.src, **config), render_string(self.dst, **config))
        return None
