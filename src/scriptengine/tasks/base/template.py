"""Template task for ScriptEngine."""

from pathlib import Path
import os
import stat
import jinja2

from scriptengine.tasks.core import Task, timed_runner
from scriptengine.jinja import render as j2render
from scriptengine.jinja import filters as j2filters


class Template(Task):
    """Template task, renders a template with Jinja2 and writes result to file.

    The task needs a source (a Jinja2 template file) and a destination. It
    renders the template given the context passed in kwargs and writes the
    result to the destination file.

    Args:
        dictionary (dict): Must at least contain the following keys:
            - src: Source file name (a Jinja2 template)
            - dst: Destination file name
    """

    _required_arguments = (
        "src",
        "dst",
    )

    def __init__(self, arguments):
        Template.check_arguments(arguments)
        super().__init__(arguments)

    def __str__(self):
        return f"Template: {self.src} --> {self.dst}"

    @timed_runner
    def run(self, context):
        src = self.getarg("src", context)
        dst = Path(self.getarg("dst", context))
        self.log_info(f"Jinja2 render: {src} --> {dst}")

        # Prepare the Jinja render environment with the proper search path
        search_path = (
            Path("."),
            Path(".") / "templates",
            Path(context["se"]["cli"]["cwd"]),
            Path(context["se"]["cli"]["cwd"]) / "templates",
        )
        self.log_debug(f"Template search path: {tuple(map(str, search_path))}")
        j2loader = jinja2.FileSystemLoader(search_path)
        j2env = jinja2.Environment(loader=j2loader)
        for name, function in j2filters().items():
            j2env.filters[name] = function

        output = j2render(j2env.get_template(src).render(context), context)
        with dst.open(mode="w") as f:
            f.write(output + "\n")

        if self.getarg("executable", context, default=False):
            umask = os.umask(0)
            os.umask(umask)
            dst.chmod(
                dst.stat().st_mode
                | (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) & ~umask
            )
