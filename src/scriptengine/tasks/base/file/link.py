from glob import glob
from pathlib import Path

from scriptengine.exceptions import (
    ScriptEngineTaskArgumentMissingError,
    ScriptEngineTaskRunError,
)
from scriptengine.tasks.core import Task, timed_runner


class Link(Task):
    """SE base.link task, creates symlinks:

        base.link:
            link: <link>  # optional, defaults to '.'
            target: <target>

    where <link> is a file or directory name and <target> is a file/directory
    name, a glob pattern, or a list thereof. If it is a glob pattern or a list,
    <link> must be a directory.  A symlink with the specified name is created
    that points to the target. If the link name is an existing directory, the
    symlink named after the target basename is created inside this directory.
    When multiple targets are specified (list or glob pattern) the links are
    created inside the <link> directory for each target.
    """

    #   _required_arguments = ("target",)

    def __init__(self, arguments):
        Link.check_arguments(arguments)
        super().__init__(arguments)

    @timed_runner
    def run(self, context):

        target_arg = self.getarg("src", context, default=False)
        if target_arg:
            self.log_warning("The 'src' argument is deprecated, use 'target' instead!")
        else:
            target_arg = self.getarg("target", context, default=False)
            if not target_arg:
                self.log_error("Missing 'target' argument")
                raise ScriptEngineTaskArgumentMissingError

        link_arg = self.getarg("dst", context, default=False)
        if link_arg:
            self.log_warning("The 'dst' argument is deprecated, use 'link' instead!")
        else:
            link_arg = self.getarg("link", context, default=".")

        self.log_info(f"Link: '{link_arg}' --> '{target_arg}'")

        target_list = []
        for t in target_arg if isinstance(target_arg, list) else [target_arg]:
            try:
                target_list.extend(glob(t))
            except TypeError as e:
                self.log_error(f"Argument error in 'target': {e}")
                raise ScriptEngineTaskRunError
        self.log_debug(f"Link targets: {target_list}")

        if not target_list:
            self.log_warning("No valid targets, therefore no links created")
            return

        try:
            link = Path(link_arg)
        except TypeError as e:
            self.log_error(f"Argument error in 'link': {e}")
            raise ScriptEngineTaskRunError

        if len(target_list) > 1 and not link.is_dir():
            self.log_error("If multiple targets are given, link must be a directory")
            raise ScriptEngineTaskRunError

        for target in (Path(t) for t in target_list):
            if link.is_dir():
                (link / target.name).symlink_to(target)
            else:
                link.symlink_to(target)
