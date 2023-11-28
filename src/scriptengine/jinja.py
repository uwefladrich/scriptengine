"""ScriptEngine helpers: Jinja2 rendering"""

import datetime
import os

import jinja2

from scriptengine.exceptions import ScriptEngineParseJinjaError


def string_to_datetime(string, format="%Y-%m-%d %H:%M:%S"):
    """Jinja2 filter to convert a string to datetime.datetime"""
    return datetime.datetime.strptime(string, format)


def string_to_date(string, format="%Y-%m-%d %H:%M:%S"):
    """Jinja2 filter to convert a string to datetime.date"""
    return datetime.datetime.strptime(string, format).date()


def basename(path):
    """Jinja2 filter that returns a path's base name"""
    return os.path.basename(path)


def dirname(path):
    """Jinja2 filter that returns a path's dir name"""
    return os.path.dirname(path)


def exists(path):
    """Jinja2 filter that returns whether a path exists or not"""
    return os.path.exists(path)


def path_join(pathlist):
    """Jinja2 filter that composes a path from components"""
    return os.path.join(*pathlist)


def filters():
    """Return all defined Jinja2 filters by their name and corresponding function"""
    return {
        "datetime": string_to_datetime,
        "date": string_to_date,
        "basename": basename,
        "dirname": dirname,
        "exists": exists,
        "path_join": path_join,
    }


# Jinja2 Environment to be used for rendering of parameters in the YAML files
_param_env = jinja2.Environment(loader=jinja2.BaseLoader)
for name, function in filters().items():
    _param_env.filters[name] = function


def _strtobool(value):
    if value in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif value in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"Cannot convert '{value}' to a boolean value")


def render(arg, context, recursive=True, boolean=False):
    """Renders a string with Jinja2.

    The argument is rendered via jinja2.Template().render() if it is a string,
    or returned unchanged otherwise. Rendering is done either once or
    recursively until no further variables can be substituted. The result is
    returned either as string, or converted into a bool (True/False).

    Args:
        arg: The string to be rendered. If it is not a string, arg is returned
            without changes.
        recursive (bool): If true (default), the string is rendered
            recursively, i.e. until it's value doesn't change anymore. If
            false, the string is rendered once.
        boolean (bool): If false (default) the rendered string is returned
            (i.e. the return value is a string). If true, the rendered
            string is evaluated in a boolean context in Jinja2.  The return
            value is true or false in this case.
        context (dict): A dictionary that provides the context for
            jinja2.Template().render()

    Returns:
        str: The rendered string (of boolean==False), OR
        bool: The rendered string, evaluated as bool (if boolean=True)
    """

    def render_with_context(string_arg):
        try:
            # Render string in parameter environment using context
            return _param_env.from_string(string_arg).render(context)
        except jinja2.TemplateError as e:
            raise ScriptEngineParseJinjaError(
                f"Jinja2 {type(e).__name__} while parsing '{string_arg}'"
                f"{' (in boolean context): ' if boolean else ': '}"
                f"{e}"
            )

    if isinstance(arg, str):
        rendered_string = render_with_context(arg)
        if recursive:
            next_rendered_string = render_with_context(rendered_string)
            while rendered_string != next_rendered_string:
                rendered_string = next_rendered_string
                next_rendered_string = render_with_context(rendered_string)
        if boolean:
            expr = f"{{% if {rendered_string} %}}1{{% else %}}0{{% endif %}}"
            return _strtobool(render_with_context(expr))
        return rendered_string
    else:
        return arg
