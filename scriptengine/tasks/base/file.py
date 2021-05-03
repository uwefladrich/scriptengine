"""ScriptEngine file tasks
Provides Copy, Move, Link, Remove and MakeDir tasks
"""

import pathlib
import shutil

from scriptengine.tasks.core import Task, timed_runner
from scriptengine.exceptions import ScriptEngineTaskRunError


def _getarg_path(self, name, context={}, **kwargs):
    """Wrapper for Task.getarg() that returns a pathlib.Path"""
    arg = self.getarg(name, context, **kwargs)
    try:
        return pathlib.Path(arg)
    except TypeError:
        self.log_error(
            f'Invalid "{name}" argument, "{arg}" is not a path'
        )
        raise ScriptEngineTaskRunError


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

        src = _getarg_path(self, 'src', context)
        dst = _getarg_path(self, 'dst', context)

        if src.is_file():
            self.log_info(f'Copy file: {src} --> {dst}')
            if dst.exists():
                self.log_warning(
                    f'Destination file "{dst}" exists already; overwriting')
            shutil.copy(src, dst)
        elif src.is_dir():
            self.log_info(f'Copy directory: {src} --> {dst}')
            if dst.exists():
                self.log_error(
                    f'Target directory "{dst}" exists'
                )
                raise ScriptEngineTaskRunError
            shutil.copytree(str(src), str(dst), symlinks=True)
        elif not src.exists():
            ignore = self.getarg('ignore_not_found', context, default=False)
            if ignore:
                self.log_warning(
                    f'"src" does not exist: {src}'
                )
            else:
                self.log_error(
                    f'"src" does not exist: {src}'
                )
                raise ScriptEngineTaskRunError
        else:
            self.log_error(
                f'"src" is not a file or directory: {src}'
            )
            raise ScriptEngineTaskRunError


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
        src = _getarg_path(self, 'src', context)
        dst = _getarg_path(self, 'dst', context)
        self.log_info(f'Move file: {src} --> {dst}')
        shutil.move(str(src), str(dst))


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
        src = _getarg_path(self, 'src', context)
        dst = _getarg_path(self, 'dst', context)
        self.log_info(f'Create link: {src} --> {dst}')
        dst.symlink_to(src)
        if not dst.exists():
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
        path = _getarg_path(self, 'path', context)
        if path.exists():
            if path.is_dir():
                self.log_info(f'Removing directory "{path}"')
                shutil.rmtree(str(path))
            else:
                self.log_info(f'Removing "{path}"')
                path.unlink()
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
        path = _getarg_path(self, 'path', context)
        try:
            path.mkdir(parents=True)
        except FileExistsError:
            if path.is_dir():
                self.log_info(
                    f'Directory "{path}" exists already'
                )
            else:
                self.log_error(
                    f'A file in the way of creating directory "{path}"'
                )
                raise ScriptEngineTaskRunError
        else:
            self.log_info(
                f'Created directory "{path}"'
            )
