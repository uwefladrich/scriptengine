"""ScriptEngine command line interface (cli).

The se command provides a command line interface to ScriptEngine, allowing for
the creation of scripts from YAML files and running the scripts via the
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


import argparse
import importlib.metadata
import logging
import os

import scriptengine.helpers.terminal_colors
import scriptengine.logging
from scriptengine.engines import SimpleScriptEngine
from scriptengine.exceptions import ScriptEngineParseError, ScriptEngineParseFileError
from scriptengine.tasks.core.loader import load as load_tasks
from scriptengine.yaml.parser import parse_file as parse_yaml_file

__version__ = importlib.metadata.version("scriptengine")


def parse_cmd_line_args():
    """Parses the command line arguments with argparse"""
    arg_parser = argparse.ArgumentParser(
        description="ScriptEngine command line tool",
        epilog="Available ScriptEngine tasks: " + ", ".join(load_tasks().keys()),
    )
    arg_parser.add_argument(
        "-V",
        "--version",
        help="show ScriptEngine version and exit",
        action="version",
        version=__version__,
    )
    arg_parser.add_argument(
        "--loglevel",
        help="The minimum level of log messages that is "
        "displayed. For verbose output, use "
        '"debug". For minimal output, use "error" '
        'or "critical".',
        choices=["debug", "info", "warning", "error", "critical"],
    )
    arg_parser.add_argument(
        "--nocolor", help="do not use colored terminal output", action="store_true"
    )
    arg_parser.add_argument("files", help="YAML file(s) to read", nargs="+")

    return arg_parser.parse_args()


def parse_files(logger, files):
    """Parses files and returns a script (list of tasks/jobs)."""
    script = []
    for fname in files:
        # next_script is a Task or Job or list of either
        next_script = parse_yaml_file(fname)
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
      context['se']['cli']['cwd']         - the original working directory
      context['se']['cli']['script_path'] - list of paths for all scripts
                                            given at the command line (used
                                            as search path for includes, for
                                            example)
      context['se']['instance']           - a reference to the ScriptEngine
                                            instance that executes the task
      context['se']['tasks']['timing']    - task timing information
                                            (defaults to no timing)
    """

    # Parse command line arguments
    parsed_args = parse_cmd_line_args()

    # Choose colored output unless --nocolor
    scriptengine.helpers.terminal_colors.set_theme(
        "none" if parsed_args.nocolor else "standard"
    )

    # Configure logging with level given by --loglevel
    # or by default with logging.INFO
    scriptengine.logging.configure(
        logging.getLevelName(parsed_args.loglevel.upper())
        if parsed_args.loglevel
        else logging.INFO
    )
    logger = logging.getLogger("se.cli")
    logger.info("Logging configured and started")

    # Log all loaded tasks if debugging
    if logger.level <= logging.DEBUG:
        for name, task in load_tasks().items():
            logger.debug(
                f"Loaded task {name}: {task.__name__} " f"from {task.__module__}"
            )

    # Create script by parsing the files given on the command line
    try:
        script = parse_files(logger, parsed_args.files)
    except ScriptEngineParseFileError:
        logger.critical("Could not read all script files")
        return os.EX_NOINPUT
    except ScriptEngineParseError:
        logger.critical("Could not parse all script files")
        return os.EX_DATAERR

    # Collect paths (and remove duplicates)
    script_path = tuple(
        dict.fromkeys((os.path.dirname(file) for file in parsed_args.files))
    )

    context = {
        "se": {
            "cli": {
                "cwd": os.getcwd(),
                "script_path": script_path,
            },
            "tasks": {
                "timing": {
                    "mode": None,
                    "logging": None,
                    "timers": {},
                },
            },
            "instance": SimpleScriptEngine(),
        }
    }

    # Call ScriptEngine instance to run the script
    context["se"]["instance"].run(script, context)

    return os.EX_OK
