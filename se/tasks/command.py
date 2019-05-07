import ast
import subprocess

from se.tasks import Task
from se.helpers import render_string_recursive


class Command(Task):

    def __init__(self, dict):
        super(Command, self).__init__(dict, 'name')

    def __str__(self):
        return 'Running command "{}" with arguments "{}"'.format(self.name,
                                                                 getattr(self, 'args', None))

    def run(self, *, dryrun=False, **config):
        if dryrun:
            print(render_string_recursive(str(self), **config))
        else:
            args = getattr(self, 'args', [])
            if type(args) is str:
                try:
                    args = ast.literal_eval(render_string_recursive(args, **config))
                except ValueError:
                    raise RuntimeError('Found invalid args expression: {}'.format(args))
            if hasattr(self, 'cwd'):
                cwd = render_string_recursive(self.cwd, **config)
            else:
                cwd = None
            subprocess.run([self.name]+args, cwd=cwd)
        return None
