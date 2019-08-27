"""ScriptEngine helpers: Jinja2 rendering"""

from distutils.util import strtobool
from jinja2 import Template, TemplateSyntaxError


def render_string(string, context, recursive=True, boolean=False):
    """ Renders a string with Jinja2.

    The string is rendered via jinja2.Template().render(), either once or
    recursively until no further variables can be substituted. The result is
    returned either as string, or converted into a bool (True/False).

    Args:
        string (str): The string to be rendered
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
            return Template(string_arg).render(context)
        except TemplateSyntaxError:
            raise RuntimeError(f"Syntax error while rendering template string '{string}'"
                               f"{' in boolean context' if boolean else ''}")

    rendered_string = render_with_context(string)
    if recursive:
        next_rendered_string = render_with_context(rendered_string)
        while rendered_string != next_rendered_string:
            rendered_string = next_rendered_string
            next_rendered_string = render_with_context(rendered_string)
    if boolean:
        expr = f"{{% if {rendered_string} %}}1{{% else %}}0{{% endif %}}"
        return bool(strtobool(render_with_context(expr)))
    return rendered_string
