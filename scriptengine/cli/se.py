"""ScriptEngine command line interface (cli).

The se command provides a command line interface to ScriptEngine, allowing for
the creation of scripts from YAML files and runnig the scripts via the
SimpleScriptEngine.
"""

__copyright__ = """
Copyright 2019, 2020 Uwe Fladrich

This file is part of ScriptEngine.

ScriptEngine is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ScriptEngine is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ScriptEngine. If not, see <https://www.gnu.org/licenses/>.
"""
__license__ = "GPLv3+"


import os
import argparse
import logging

from attrdict import AttrDict

import scriptengine.version
import scriptengine.logging

from scriptengine.helpers import terminal_colors
from scriptengine.scripts import SimpleScriptEngine

from scriptengine.exceptions import ScriptEngineParseError

__version__ = scriptengine.version.__version__


def parse_cmd_line_args():
    """Parses the command line arguments with argparse
    """
    arg_parser = argparse.ArgumentParser(
                        description="ScriptEngine command line tool")

    arg_parser.add_argument("-V", "--version",
                            help="show ScriptEngine version and exit",
                            action="version",
                            version=__version__)
    arg_parser.add_argument("-q", "--quiet",
                            help="be quiet, no extra output",
                            action="store_true")
    arg_parser.add_argument("--debug",
                            help="lots of extra debug output",
                            action="store_true")
    arg_parser.add_argument("--nocolor",
                            help="do not use colored terminal output",
                            action="store_true")
    arg_parser.add_argument("files",
                            help="YAML file(s) to read",
                            nargs="+")

    return arg_parser.parse_args()


def configure_loggers(nocolor=False, quiet=False, debug=False):
    """Configures logging according to arguments:
       - sets color scheme (side effect!)
       - creates cli, task, se instance loggers with appropriate levels
    """
    if nocolor:
        terminal_colors.set_theme("none")

    if quiet:
        log_level = logging.WARNING
    elif debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Configure CLI logger
    scriptengine.logging.configure_logger(
            'se.cli', log_level, scriptengine.logging.cli_log_formatter)

    # Configure Task logger
    scriptengine.logging.configure_logger(
            'se.task', log_level, scriptengine.logging.task_log_formatter)

    # Configure Job logger
    # Uses same formatting as Task logger!
    scriptengine.logging.configure_logger(
            'se.job', log_level, scriptengine.logging.task_log_formatter)

    # Configure SE instance logger
    # Uses same formatting as CLI logger!
    scriptengine.logging.configure_logger(
            'se.instance', log_level, scriptengine.logging.cli_log_formatter)

    cli_logger = logging.getLogger('se.cli')
    cli_logger.info('Logging configured and started')

    return cli_logger


def parse_files(logger, files):
    """Parses files and returns a script (list of tasks/jobs).
    """
    script = []
    for fname in files:
        try:
            # next_script is a Task or Job or list of either
            next_script = scriptengine.yaml.parse_file(fname)
        except ScriptEngineParseError as e:
            logger.error(f'{e} in {fname}')
            raise
        if isinstance(next_script, list):
            script.extend(next_script)
        else:
            script.append(next_script)

    return script


def main():
    """ScriptEngine command line tool

       The context is passed to the ScriptEngine instance and, later, to all
       tasks. Some context information is already set here in the se command
       line tool:
         context.se.cli.cwd         - the original working directory
         context.se.cli.script_path - list of paths for all scripts given at
                                      the command line (used as search path
                                      for includes, for example)
         context.se.instance        - a reference to the ScriptEngine instance
                                      that executes the task
         context.se.tasks.timing    - task timing information
                                      (defaults to no timing)
    """

    # parse command line arguments
    parsed_args = parse_cmd_line_args()

    # set up logging
    #   - logs for cli, tasks, jobs, se instances
    #   - color scheme
    logger = configure_loggers(nocolor=parsed_args.nocolor,
                               quiet=parsed_args.quiet,
                               debug=parsed_args.debug)

    # create script by parsing the files given on the command line
    script = parse_files(logger, parsed_args.files)

    # Note that the following removal of duplicates does not guarantee the
    # order of entries before Python 3.7! We'll accept this in favour of the
    # easier implementation.
    script_path = tuple(dict.fromkeys(
                        (os.path.dirname(file) for file in parsed_args.files)))

    # Initialise the context as AttrDict,
    # i.e. allowing *read* access as, for example, 'context.se.cli.cwd'
    context = AttrDict({
        'se': {
            'cli': {
                'cwd': os.getcwd(),
                'script_path': script_path,
            },
            'tasks': {
                'timing': {
                    'mode': None,
                    'logging': None,
                    'timers': {},
                },
            },
            'instance': SimpleScriptEngine(),
        }
    })

    # call ScriptEngine instance to run the script
    context.se.instance.run(script, context)

    return 0
