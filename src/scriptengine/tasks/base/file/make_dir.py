from pathlib import Path

from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.tasks.core import Task, timed_runner


class MakeDir(Task):
    """SE base.make_dir task, creates directories:

        base.make_dir:
            path: <dir_path>

    where <dir_path> is the name of the new directory or list of such.
    If a directory exists already, a warning is written and SE continues. If a
    file with the same name exists, a ScriptEngineTaskRunError is raised.
    """

    _required_arguments = ("path",)

    def __init__(self, arguments):
        MakeDir.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):

        path_arg = self.getarg("path", context)
        self.log_info(f"MakeDir: {path_arg}")

        for path in (
            Path(p) for p in (path_arg if isinstance(path_arg, list) else [path_arg])
        ):
            self.log_debug(f"Create directory '{path}'")
            try:
                path.mkdir(parents=True)
            except FileExistsError as e:
                if path.is_dir():
                    self.log_warning(f"Error creating '{path}': {e}")
                else:
                    self.log_error(
                        f"File '{path}' exists already, can not create directory"
                    )
                    raise ScriptEngineTaskRunError
