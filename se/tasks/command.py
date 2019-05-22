import logging
import ast
import subprocess

from se.tasks import Task
from se.helpers import render_string_recursive

log = logging.getLogger(__name__)

class Command(Task):

    def __init__(self, dict):
        super(Command, self).__init__(dict, 'name')
        log.debug('Creating "{}"'.format(dict))

    def __str__(self):
        return 'Running command "{}" with arguments "{}"'.format(self.name,
                                                                 getattr(self, 'args', None))

    def run(self, *, dryrun=False, **config):
        log.info('{} {}'.format(render_string_recursive(str(self.name), **config),
                                render_string_recursive(str(getattr(self, 'args', ''), **config))))
        if dryrun:
            print(render_string_recursive(str(self), **config))
            return None

        command = render_string_recursive(self.name, **config)
        arglist = getattr(self, 'args', [])
        if type(arglist) is str:
            try:
                arglist = ast.literal_eval(render_string_recursive(arglist, **config)) or []
            except ValueError:
                raise RuntimeError('Command task: can''t parse "args": {}'.format(arglist))
        else:
            try:
                arglist = [render_string_recursive(arg, **config) for arg in arglist]
            except TypeError:
                raise RuntimeError('Command task: "args" not iterable: {}'.format(arglist))
        cwd = render_string_recursive(self.cwd, **config) if hasattr(self, 'cwd') else None
        subprocess.run([command]+arglist, cwd=cwd)
        return None
