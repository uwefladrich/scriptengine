"""Copy task for ScriptEngine."""

import shutil

from se.tasks import Task
from se.helpers import render_string

class Copy(Task):
    """Copy task, copies a file.

    The task needs a source and a destination and copies a file with the shutil
    module.

    Args:
        dictionary (dict): Must at least contain the following keys:
            - src: Source file name
            - dst: Destination file or directory name
    """
    def __init__(self, dictionary):
        super().__init__(__name__, dictionary, 'src', 'dst')

    def __str__(self):
        return f'Copy: {self.src} --> {self.dst}'

    def run(self, **kwargs):
        self.log_info(f'{render_string(self.src, **kwargs)} '
                      f'--> {render_string(self.dst, **kwargs)}')
        if getattr(kwargs, 'dryrun', False):
            print(render_string(str(self), **kwargs))
        else:
            shutil.copy(render_string(self.src, **kwargs), render_string(self.dst, **kwargs))
