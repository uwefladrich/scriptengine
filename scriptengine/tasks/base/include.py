"""Include task for ScriptEngine

   The Include task reads a YAML file, parses the content to create a
   ScriptEngine script and lets the active ScriptEngine instance execute it.
"""

import os

from scriptengine.yaml.parser import parse_file as parse_yaml_file

from scriptengine.tasks.core import Task, timed_runner
from scriptengine.exceptions import ScriptEngineTaskRunError


class Include(Task):

    _required_arguments = ('src', )

    def __init__(self, arguments):
        Include.check_arguments(arguments)
        super().__init__(arguments)

    def __str__(self):
        return f'Include: {self.src}'

    @timed_runner
    def run(self, context):
        inc_file = self.getarg('src', context)
        self.log_info(f'Include script from {inc_file}')

        search_path = (
            '.',
            context['se']['cli']['cwd'],
            *context['se']['cli']['script_path'],
        )
        self.log_debug(f'Searching in path: {search_path}')

        for directory in search_path:
            inc_file_path = os.path.join(directory, inc_file)
            self.log_debug(f'Searching for include file at "{inc_file_path}"')
            if os.path.isfile(inc_file_path):
                self.log_debug(f'Found include file at "{inc_file_path}"')
                break
        else:
            if self.getarg('ignore_not_found', default=False):
                self.log_warning(f'Include file "{inc_file}" not found.')
                return
            msg = f'Include file "{inc_file}" not found'
            self.log_error(msg)
            raise ScriptEngineTaskRunError(msg)

        script = parse_yaml_file(inc_file_path)

        inc_file_dir = os.path.dirname(os.path.abspath(inc_file_path))
        if inc_file_dir not in context['se']['cli']['script_path']:
            context['se']['cli']['script_path'] += inc_file_dir,
        self.log_debug(
            f'New script_path: {context["se"]["cli"]["script_path"]}'
        )

        self.log_debug(f'Execute script from "{inc_file}"')
        context['se']['instance'].run(script, context)
        self.log_debug(f'Finished executing script from "{inc_file}"')
