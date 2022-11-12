import shutil
from glob import glob
from pathlib import Path

from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.tasks.core import Task, timed_runner


class Move(Task):
    """SE base.move task, moves files and directories:

        base.move:
            src: <source>
            dst: <destination>
            ignore_not_found: <true_or_false>  # optional

    where <source> is a file/directory name or a glob (wildcard) pattern, or a
    list with items thereof. <destination> is a file or directory name. If
    <ignore_not_found> is false (default), a ScriptEngineTaskRunError is raised
    if no source files are found. If true, only a warning is written and SE
    continues.
    """

    _required_arguments = (
        "src",
        "dst",
    )

    def __init__(self, arguments):
        Move.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):

        src_arg = self.getarg("src", context)
        dst_arg = self.getarg("dst", context)
        self.log_info(f"Move: {src_arg} --> {dst_arg}")

        sources = []
        for s in src_arg if isinstance(src_arg, list) else [src_arg]:
            try:
                sources.extend(glob(s))
            except TypeError as e:
                self.log_error(f"Argument error in 'src': {e}")
                raise ScriptEngineTaskRunError
        self.log_debug(f"Move sources: {sources}")

        if not sources:
            if self.getarg("ignore_not_found", context, default=False):
                self.log_warning("No files found to move")
                return
            else:
                self.log_error("No files found to move")
                raise ScriptEngineTaskRunError

        try:
            dst = Path(dst_arg)
        except TypeError as e:
            self.log_error(f"Argument error in 'dst': {e}")
            raise ScriptEngineTaskRunError
        self.log_debug(f"Move destination: {dst}")

        if dst.is_file():
            if len(sources) > 1:
                self.log_error("Cannot move multiple files onto one file")
                raise ScriptEngineTaskRunError
            if Path(sources[0]).is_dir():
                self.log_error("Cannot move a directory onto a file")
                raise ScriptEngineTaskRunError
            self.log_warning(f"Destination file exists, overwriting '{dst}'")

        for src in (Path(s) for s in sources):
            self.log_debug(f"Move '{src} --> {dst}")
            # shutil.move prior to 3.9 accepts only strings, not path-like objects
            shutil.move(str(src), str(dst))
