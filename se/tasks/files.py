import shutil

from se.tasks import Task
from se.helpers import render_string_recursive


class Copy(Task):

    def __init__(self, dict):
        super(Copy, self).__init__(dict, 'src', 'dst')

    def __str__(self):
        return 'Copy: {} --> {}'.format(self.src, self.dst)

    def run(self, *, dryrun=False, **kwargs):
        if dryrun:
            print(render_string_recursive(str(self), **kwargs))
        else:
            shutil.copy(render_string_recursive(self.src, **kwargs), render_string_recursive(self.dst, **kwargs))


class Link(Task):

    def __init__(self, dict):
        super(Link, self).__init__(dict, 'src', 'dst')

    def __str__(self):
        return 'Link: {} --> {}'.format(self.src, self.dst)

    def run(self):
        print(self)
