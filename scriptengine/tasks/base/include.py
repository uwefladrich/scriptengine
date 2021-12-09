"""Include task for ScriptEngine

   The Include task reads a YAML file, parses the content to create a
   ScriptEngine script and lets the active ScriptEngine instance execute it.
"""

from pathlib import Path

from deepmerge import always_merger

from scriptengine.context import context_delta, save_copy
from scriptengine.exceptions import ScriptEngineTaskRunError
from scriptengine.tasks.core import Task, timed_runner
from scriptengine.yaml.parser import parse_file


def _file_in_paths(file, paths=None):
    if file.is_absolute():
        if file.is_file():
            return file
    else:
        searched_paths = []
        for p in paths or []:
            if p not in searched_paths:
                searched_paths.append(p)
                fpath = p / file
                if fpath.is_file():
                    return fpath
    raise FileNotFoundError


class Include(Task):

    _required_arguments = ("src",)

    def __init__(self, arguments):
        Include.check_arguments(arguments)
        super().__init__(arguments)

    def __str__(self):
        return f"Include: {self.src}"

    @timed_runner
    def run(self, context):

        src = Path(self.getarg("src", context))
        self.log_info(f"Include script from {src}")

        local_context = save_copy(context)

        # Search for include file in '.', old cwd, and script_path
        cwd = Path(".")
        ocwd = Path(local_context["se"]["cli"]["cwd"])
        script_path = (Path(p) for p in local_context["se"]["cli"]["script_path"])
        search_path = (cwd, ocwd, *script_path)
        self.log_debug(
            f"Include file search path: {tuple(str(p) for p in search_path)}"
        )

        try:
            inc_file = _file_in_paths(src, search_path)
        except FileNotFoundError:
            if self.getarg("ignore_not_found", default=False):
                self.log_warning(f"Include file not found: {src}")
                return
            self.log_error(f"Include file not found: {src}")
            raise ScriptEngineTaskRunError
        self.log_debug(f"Include file found: {str(inc_file)}")

        script = parse_file(inc_file)

        self.log_debug(f"Execute include script: {inc_file}")
        context_update = local_context["se"]["instance"].run(script, local_context)
        self.log_debug(f"Finished executing include script: {inc_file}")

        return context_delta(
            context, always_merger.merge(local_context, context_update)
        )
