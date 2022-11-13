import shutil
from glob import glob
from pathlib import Path

from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.tasks.core import Task, timed_runner


class Remove(Task):
    """SE base.remove task, deletes files or directories:

        base.remove:
            path: <path>
            ignore_not_found: <true_or_false>  # optional

    where <path> is a file/directory name or a glob (wildcard) pattern, or a
    list with items thereof.
    If <ignore_not_found> is false (default), a ScriptEngineTaskRunError is
    raised if a file or directory from <path> is found. If true, only a warning
    is written and SE continues.
    """

    _required_arguments = ("path",)

    def __init__(self, arguments):
        Remove.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):

        path_arg = self.getarg("path", context)
        self.log_info(f"Remove '{path_arg}'")

        path_list = []
        for p in path_arg if isinstance(path_arg, list) else [path_arg]:
            try:
                path_list.extend(glob(p))
            except TypeError as e:
                self.log_error(f"Argument error in 'path': {e}")
                raise ScriptEngineTaskRunError
        self.log_debug(f"Remove files/dirs: {path_list}")

        if not path_list:
            if self.getarg("ignore_not_found", context, default=False):
                self.log_warning("Non-existing path, nothing to remove")
                return
            else:
                self.log_warning("Non-existing path")
                self.log_warning(
                    "Deprecation warning! base.remove has not found anything to "
                    "delete but ignore_not_found was not true. In the future, "
                    "this will lead to an error!"
                )
                return
            #   self.log_error("Non-existing path")
            #   raise ScriptEngineTaskRunError

        for path in (Path(p) for p in path_list):
            if path.is_dir():
                self.log_debug(f"Remove directory: '{path}'")
                try:
                    shutil.rmtree(path)
                except PermissionError as e:
                    self.log_error(f"Cannot remove directory: {e}")
                    raise ScriptEngineTaskRunError
            else:
                self.log_debug(f"Remove file: '{path}'")
                try:
                    path.unlink()
                except PermissionError as e:
                    self.log_error(f"Cannot remove file: {e}")
                    raise ScriptEngineTaskRunError
