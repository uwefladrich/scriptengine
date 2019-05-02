import shutil

from se.tasks import Task
from se.helpers import render_string_recursive


class Copy(Task):

    def __init__(self, dict):
        super(Copy, self).__init__(dict, 'src', 'dst')

    def __str__(self):
        return 'Copy: {} --> {}'.format(self.src, self.dst)

    def run(self, *, dryrun=False, **config):
        if dryrun:
            print(render_string_recursive(str(self), **config))
        else:
            shutil.copy(render_string_recursive(self.src, **config), render_string_recursive(self.dst, **config))
        return None


class Link(Task):

    def __init__(self, dict):
        super(Link, self).__init__(dict, 'src', 'dst')

    def __str__(self):
        return 'Link: {} --> {}'.format(self.src, self.dst)

    def run(self, *, dryrun=False, **config):
        if dryrun:
            print(render_string_recursive(str(self), **config))
        else:
            raise NotImplementedError('Link task not yet implemented (dry-run only)')
        return None
