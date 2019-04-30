import subprocess

from se.tasks import Task
from se.helpers import render_string_recursive


class Command(Task):

    def __init__(self, dict):
        super(Command, self).__init__(dict, 'name')

    def __str__(self):
        return 'Running command "{}" with arguments "{}"'.format(self.name,
                                                                 getattr(self, 'args', None))

    def run(self, *, dryrun=False, **kwargs):
        if dryrun:
            print(render_string_recursive(str(self), **kwargs))
        else:
            cmd = [self.name] \
                + [render_string_recursive(s, **kwargs) for s in getattr(self, 'args', [])]
            subprocess.run(cmd)
