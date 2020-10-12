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


import sys
import os
import argparse
import logging

import scriptengine.version
import scriptengine.logging

from scriptengine.helpers import terminal_colors
from scriptengine.scripts import SimpleScriptEngine

from scriptengine.exceptions import ScriptEngineParseError

__version__ = scriptengine.version.__version__


CLI_LOGGER = None


def init_context(ctx):
    """Initialise context as dict with some defaults
    """
    ctx['_se_cmd_cwd'] = os.getcwd()
    ctx['_se_cmd_args'] = sys.argv

def init_config(cfg):
    """Initialise se config as dict with some defaults
    """
    cfg['se_instance_type'] = SimpleScriptEngine


def parse_config_file(cfg):
    """Parse ScriptEngine configuration files.
       Overwrite current values in config
    """


def configure_logger(cfg, ctx):
    """Configures logging according to 'cfg':
       - sets color scheme (side effect!)
       - creates cli, task, se instance loggers with appropriate levels
    """
    if cfg["nocolor"]:
        terminal_colors.set_theme("none")

    if cfg["quiet"]:
        log_level = logging.WARNING
    elif cfg["debug"]:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Configure CLI logger
    scriptengine.logging.configure_logger(
            'se.cli', log_level, scriptengine.logging.cli_log_formatter)
    global CLI_LOGGER
    CLI_LOGGER = logging.getLogger('se.cli')

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

    CLI_LOGGER.info('Logging configured and started')


def process_cmd_line_args(cfg):
    """Parses the command line arguments and modifies the confuguration accordingly
    """
    arg_parser = argparse.ArgumentParser(description="ScriptEngine command line tool")

    arg_parser.add_argument("-V", "--version", help="show ScriptEngine version and exit",
                            action="version", version=__version__)
    arg_parser.add_argument("-t", "--taskset", help="load taskset", action="append")
    arg_parser.add_argument("-q", "--quiet", help="be quiet, no extra output", action="store_true")
    arg_parser.add_argument("--debug", help="lots of extra debug output", action="store_true")
    arg_parser.add_argument("--nocolor", help="do not use colored terminal output",
                            action="store_true")
    arg_parser.add_argument("file", help="YAML file(s) to read", nargs="+")

    args = arg_parser.parse_args()

    cfg['files'] = args.file
    cfg['taskset'] = args.taskset
    cfg['quiet'] = args.quiet
    cfg['debug'] = args.debug
    cfg['nocolor'] = args.nocolor


def load_tasks(cfg, ctx):
    """Loads tasks from scriptengine.tasks.base, plus whatever is in the config
    """
    taskset = ["base"] + (cfg["taskset"] or [])
    scriptengine.tasks.base.load([f"scriptengine.tasks.{ts}" for ts in taskset])
    CLI_LOGGER.debug(
        f"Loaded tasks: {', '.join(scriptengine.tasks.base.loaded_tasks().keys())}"
    )


def parse_files(cfg, ctx):
    """Parses all files named in ctx['files'] and returns a script (list of
       tasks/jobs). Add file dirnames to ctx['_se_filepath']
    """
    script = []
    for fname in cfg['files']:
        try:
            # next_script is a Task or Job or list of either
            next_script = scriptengine.yaml.parse_file(fname)
        except ScriptEngineParseError as e:
            CLI_LOGGER.error(f'{e} in {fname}')
            raise
        if isinstance(next_script, list):
            script.extend(next_script)
        else:
            script.append(next_script)
        dname = os.path.dirname(os.path.abspath(fname))
        if dname not in ctx.get('_se_filepath', []):
            ctx.setdefault('_se_filepath', []).append(dname)
    return script


def configure_scriptengine(cfg, ctx):
    """Configure the ScriptEngine instance in the context.
       Use values from configuration dict.
    """
    ctx['_se_instance_type'] = cfg['se_instance_type']
    ctx['_se_instance'] = cfg['se_instance_type']()


def main():
    """ScriptEngine command line tool

       Make sure to distinguish config and context!

       "config" stores configuration for the se command line tool
       The context is passed to the ScriptEngine instance and, later, to all
       tasks. Some context information is already set here in the se command
       line tool:
         context['_se_cmd_cwd']   - the original working directory
         context['_se_cmd_args']  - the list of arguments
         context['_se_instance']  - a reference to the ScriptEngine instance
                                    that executes the task
    """

    config = {}
    context = {}

    # initialise context
    init_context(context)

    # initialise default config
    init_config(config)

    # parse config file
    parse_config_file(config)

    # parse command line arguments
    process_cmd_line_args(config)

    # set up logging
    #   - logs for cli, tasks, jobs, se instances
    #   - color scheme
    configure_logger(config, context)

    # load tasks
    load_tasks(config, context)

    # create script by parsing the files given on the command line
    script = parse_files(config, context)

    # init scriptengine instance
    #   sets context['_se_instance']
    configure_scriptengine(config, context)

    # call ScriptEngine instance to run the script
    context['_se_instance'].run(script, context)

    return 0
