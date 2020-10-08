"""ScriptEngine file tasks
Provides Copy, Move, Link, Remove and MakeDir tasks
"""

import os
import shutil

from scriptengine.tasks.base import Task
from scriptengine.tasks.base.timing import timed_runner
from scriptengine.exceptions import ScriptEngineTaskRunError


class Copy(Task):
    """ScriptEngine Copy task: Copies files or directories. It needs 'src' and
    'dst' parameters when it is created, providing the source and destination
    paths for the copy operation. Directories are copied recursively,
    maintaining symlinks.
    """
    _required_arguments = ('src', 'dst', )

    def __init__(self, arguments):
        Copy.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        src = self.getarg('src', context)
        dst = self.getarg('dst', context)
        if os.path.isfile(src):
            self.log_info(f'Copy file: {src} --> {dst}')
            if os.path.isfile(dst):
                self.log_warning(
                    f'Destination file "{dst}" exists already; overwriting')
            shutil.copy(src, dst)
        else:
            self.log_info(f'Copy directory: {src} --> {dst}')
            if os.path.exists(dst):
                msg = f'Target "{dst}" for directory copy exists already'
                self.log_error(msg)
                raise ScriptEngineTaskRunError(msg)
            shutil.copytree(src, dst, symlinks=True)


class Move(Task):
    """ScriptEngine Move task: Moves files or directories. It needs 'src' and
    'dst' parameters when it is created, providing the source and destination
    paths for the move operation.
    """
    _required_arguments = ('src', 'dst', )

    def __init__(self, arguments):
        Move.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        src = self.getarg('src', context)
        dst = self.getarg('dst', context)
        self.log_info(f'Move file: {src} --> {dst}')
        shutil.move(src, dst)


class Link(Task):
    """ScriptEngine Link task: Creates symlinks. It needs 'src' and 'dst'
    parameters when it is created, providing the source and destination paths
    for the link.
    """
    _required_arguments = ('src', 'dst', )

    def __init__(self, arguments):
        Link.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        src = self.getarg('src', context)
        dst = self.getarg('dst', context)
        self.log_info(f'Create link: {src} --> {dst}')
        os.symlink(src, dst)
        if not os.path.exists(dst):
            self.log_warning(f'Created dangling symlink: {dst}-->{src}')


class Remove(Task):
    """ScriptEngine Remove task: Removes (deletes) files or directories.
    Directories are removed recursively. It needs the 'path' parameter when it
    is created, providing the path to the file or directory to be removed.
    """
    _required_arguments = ('path', )

    def __init__(self, arguments):
        Remove.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        path = self.getarg('path', context)
        if os.path.exists(path):
            if os.path.isdir(path):
                self.log_info(f'Removing directory "{path}"')
                shutil.rmtree(path)
            else:
                self.log_info(f'Removing file "{path}"')
                os.remove(path)
        else:
            self.log_info(f'Non-existing path "{path}"; nothing removed')


class MakeDir(Task):
    """ScriptEngine MakeDir task: Creates a directory. It needs the 'path'
    parameter when it is created, providing the path of the new directory
    """
    _required_arguments = ('path', )

    def __init__(self, arguments):
        MakeDir.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        path = self.getarg('path', context)
        if os.path.isdir(path):
            self.log_info(f'Directory "{path}" exists already.')
        elif os.path.isfile(path):
            msg = f'Can\'t create directory because "{path}" is a file'
            self.log_error(msg)
            raise ScriptEngineTaskRunError(msg)
        else:
            self.log_info(f'Creating directory "{path}"')
            os.makedirs(path)
