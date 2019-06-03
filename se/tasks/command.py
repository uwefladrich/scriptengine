import ast
import subprocess

from se.tasks import Task
from se.helpers import render_string


class Command(Task):

    def __init__(self, dict):
        super(Command, self).__init__(__name__, dict, 'name')
        self.log_debug('Creating "{}"'.format(dict))

    def __str__(self):
        return 'Running command "{}" with arguments "{}"'.format(self.name,
                                                                 getattr(self, 'args', None))

    def run(self, *, dryrun=False, **config):
        self.log_info('{} {}'.format(render_string(str(self.name), **config),
                                     render_string(str(getattr(self, 'args', ''), **config))))
        if dryrun:
            print(render_string(str(self), **config))
            return None

        command = render_string(self.name, **config)
        arglist = getattr(self, 'args', [])
        if type(arglist) is str:
            try:
                arglist = ast.literal_eval(render_string(arglist, **config)) or []
            except ValueError:
                raise RuntimeError('Command task: can''t parse "args": {}'.format(arglist))
        else:
            try:
                arglist = [render_string(arg, **config) for arg in arglist]
            except TypeError:
                raise RuntimeError('Command task: "args" not iterable: {}'.format(arglist))
        cwd = render_string(self.cwd, **config) if hasattr(self, 'cwd') else None
        subprocess.run([command]+arglist, cwd=cwd)
        return None
