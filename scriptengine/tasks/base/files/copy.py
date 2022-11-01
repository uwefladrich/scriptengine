import shutil
from glob import glob
from pathlib import Path

from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.tasks.core import Task, timed_runner


class Copy(Task):
    """SE base.copy task, copies files and directories:

        base.copy:
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
        Copy.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):

        src_arg = self.getarg("src", context)
        dst_arg = self.getarg("dst", context)
        self.log_info(f"Copy: {src_arg} --> {dst_arg}")

        sources = []
        for s in src_arg if isinstance(src_arg, list) else [src_arg]:
            try:
                sources.extend(glob(s))
            except TypeError as e:
                self.log_error(f"Argument error in 'src': {e}")
                raise ScriptEngineTaskRunError
        self.log_debug(f"Copy sources: {sources}")

        if not sources:
            if self.getarg("ignore_not_found", context, default=False):
                self.log_warning("No files found to copy")
                return
            else:
                self.log_error("No files found to copy")
                raise ScriptEngineTaskRunError

        try:
            dst = Path(dst_arg)
        except TypeError as e:
            self.log_error(f"Argument error in 'dst': {e}")
            raise ScriptEngineTaskRunError
        self.log_debug(f"Copy destination: {dst}")

        if dst.is_file():
            if len(sources) > 1:
                self.log_error("Cannot copy multiple files onto one file")
                raise ScriptEngineTaskRunError
            if Path(sources[0]).is_dir():
                self.log_error("Cannot copy a directory onto a file")
                raise ScriptEngineTaskRunError
            self.log_warning(f"Destination file exists, overwriting '{dst}'")

        for src in (Path(s) for s in sources):
            if src.is_file():
                self.log_debug(f"Copy file '{src} --> {dst}")
                shutil.copy(src, dst)
            elif src.is_dir():
                self.log_debug(f"Copy directory '{src} --> {dst}")
                shutil.copytree(src, dst, symlinks=True)
            else:
                self.log_error(f"'src' is not a valid file or directory: '{src}'")
                raise ScriptEngineTaskRunError
