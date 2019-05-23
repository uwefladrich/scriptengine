import shutil

from se.tasks import Task
from se.helpers import render_string_recursive

class Copy(Task):

    def __init__(self, dict):
        super(Copy, self).__init__(__name__, dict, 'src', 'dst')
        self.log.debug('Creating "{}"'.format(dict))

    def __str__(self):
        return 'Copy: {} --> {}'.format(self.src, self.dst)

    def run(self, *, dryrun=False, **config):
        self.log.info('{} --> {}'.format(render_string_recursive(self.src, **config),
                                         render_string_recursive(self.dst, **config)))
        if dryrun:
            print(render_string_recursive(str(self), **config))
        else:
            shutil.copy(render_string_recursive(self.src, **config), render_string_recursive(self.dst, **config))
        return None
