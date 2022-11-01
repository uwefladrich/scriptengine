"""ScriptEngine file tasks
Provides Copy, Move, Link, Remove and MakeDir tasks
"""

import pathlib
import shutil

from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.tasks.core import Task, timed_runner


def _getarg_path(self, name, context={}, **kwargs):
    """Wrapper for Task.getarg() that returns a pathlib.Path"""
    arg = self.getarg(name, context, **kwargs)
    try:
        return pathlib.Path(arg)
    except TypeError:
        self.log_error(f'Invalid "{name}" argument, "{arg}" is not a path')
        raise ScriptEngineTaskRunError


class Link(Task):
    """ScriptEngine Link task: Creates symlinks. It needs 'src' and 'dst'
    parameters when it is created, providing the source and destination paths
    for the link.
    """

    _required_arguments = (
        "src",
        "dst",
    )

    def __init__(self, arguments):
        Link.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        src = _getarg_path(self, "src", context)
        dst = _getarg_path(self, "dst", context)
        self.log_info(f"Create link: {src} --> {dst}")
        dst.symlink_to(src)
        if not dst.exists():
            self.log_warning(f"Created dangling symlink: {dst}-->{src}")


class Remove(Task):
    """ScriptEngine Remove task: Removes (deletes) files or directories.
    Directories are removed recursively. It needs the 'path' parameter when it
    is created, providing the path to the file or directory to be removed.
    """

    _required_arguments = ("path",)

    def __init__(self, arguments):
        Remove.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):
        path = _getarg_path(self, "path", context)
        if path.exists():
            if path.is_dir():
                self.log_info(f'Removing directory "{path}"')
                shutil.rmtree(str(path))
            else:
                self.log_info(f'Removing "{path}"')
                path.unlink()
        else:
            self.log_info(f'Non-existing path "{path}"; nothing removed')
