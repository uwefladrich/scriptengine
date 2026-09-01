"""Context task for ScriptEngine."""

import yaml

from scriptengine.context import (
    Context as SEContext,
)  # avoid name clashes between se.context.Context and se.tasks.base.Context
from scriptengine.exceptions import ScriptEngineTaskError, ScriptEngineTaskRunError
from scriptengine.tasks.core import Task, timed_runner


class Context(Task):
    """Context task, sets/updates the SE context.
    The context task takes name, value pairs as arguments and updates the SE
    context accordingly. Values can be scalars, lists, dictionaries and nested
    combinations thereof.
    Note that Context.run() returns a context *update* and that the higher-level
    running instance (a Job or a ScriptEngine instance) is responsible for
    merging the update with an existing context dict."""

    @timed_runner
    def run(self, context):
        context_update = SEContext(
            {n: self.getarg(n, context) for n in vars(self) if not n.startswith("_")}
        )
        self.log_info(f"Context update: {context_update}")
        return context_update


class ContextLoad(Task):
    """
    This task updates the context, just as the Context task, but from sources
    other than direct arguments.

    If the 'dict' argument is given, the argument value must be a dict and is
    used to update the context, e.g.

    - base.context:
        upd:
            foo: 1
    - base.context.load:
        dict: "{{upd}}"

    If the 'file' argument is given, the argument value must be a file name and
    the context is updated from the file context. The file format must be YAML:

    - base.context.load:
        file: update.yml
    """

    @timed_runner
    def run(self, context):
        dict_arg = self.getarg("dict", context, default=False)
        file_arg = self.getarg("file", context, default=False)

        if dict_arg and file_arg:
            self.log_error("Task arguments 'dict' and 'file' are mutual exclusive")
            raise ScriptEngineTaskError

        if dict_arg:
            self.log_info(f"Load context update from dict: {dict_arg}")
            if not isinstance(dict_arg, dict):
                self.log_error(
                    "The 'dict' argument must be a dictionary "
                    f"(was  a '{type(dict_arg).__name__}')"
                )
                raise ScriptEngineTaskRunError
            context_update_d = dict_arg

        elif file_arg:
            self.log_info(f"Load context update from file: {file_arg}")
            try:
                with open(str(file_arg)) as f:
                    dict_from_file = yaml.load(f, Loader=yaml.SafeLoader)
            except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
                self.log_error(e)
                raise ScriptEngineTaskRunError
            except yaml.scanner.ScannerError as e:
                self.log_error("Error reading the file as YAML, error message follows:")
                self.log_error(f"  {''.join(str(e).splitlines())}")
                self.log_error("Note: base.context.load supports only YAML files")
                raise ScriptEngineTaskRunError
            if not isinstance(dict_from_file, dict):
                self.log_error(
                    "Reading YAML file succeeded, but the content must be a dict "
                    f"(was a '{type(dict_from_file).__name__}')"
                )
                raise ScriptEngineTaskRunError
            context_update_d = dict_from_file

        else:
            self.log_error("Missing argument: either 'dict' or 'file' is needed")
            raise ScriptEngineTaskError

        return SEContext(context_update_d)


class ContextDump(Task):
    """
    This task dumps the context, or a subset of context keys, to a YAML file.

    Examples:
    - base.context.dump:
        file: saveic/experiment-config.yml
        root: "ic_meta"
        keys:
          - experiment
          - model_config

    - base.context.dump:
        file: all_context.yml
    """

    _required_arguments = ("file",)

    @timed_runner
    def run(self, context):
        file_arg = self.getarg("file", context)
        keys_arg = self.getarg("keys", context, default=None)
        root_arg = self.getarg("root", context, default=None)

        self.log_info(f"Dump context to file: {file_arg}")

        if keys_arg is not None:
            keys_list = [keys_arg] if isinstance(keys_arg, str) else keys_arg
            if not isinstance(keys_list, list):
                self.log_error(
                    f"The 'keys' argument must be a string or list (was a '{type(keys_arg).__name__}')"
                )
                raise ScriptEngineTaskRunError
            data = {k: context[k] for k in keys_list if k in context}
        else:
            # Dump full context excluding internal 'se' namespace
            data = {k: v for k, v in context.items() if k != "se"}

        if root_arg is not None:
            data = {str(root_arg): data}

        try:
            with open(str(file_arg), "w") as f:
                yaml.dump(data, f, sort_keys=False)
        except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as e:
            self.log_error(e)
            raise ScriptEngineTaskRunError
