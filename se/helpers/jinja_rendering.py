"""ScriptEngine helpers: Jinja2 rendering"""

from distutils.util import strtobool
from jinja2 import Template


def render_string(string, recursive=True, boolean=False, **kwargs):
    """ Renders a string with Jinja2.

    The string is rendered via jinja2.Template().render(), either once or
    recursively until no further variables can be substituted. The resulte is
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
        kwargs: A dict, a dict subclass or some keyword arguments, which
            provide the context for jinja2.Template().render()

    Returns:
        str: The rendered string (of boolean==False), or
        bool: The rendered string, evaluated as bool (if boolean=True)
    """
    rendered_string = Template(string).render(**kwargs)
    if recursive:
        while True:
            next_rendered = Template(rendered_string).render(**kwargs)
            if rendered_string == next_rendered:
                break
            else:
                rendered_string = next_rendered
    if boolean:
        expr = '{% if '+rendered_string+' %}1{% else %}0{% endif %}'
        return bool(strtobool(Template(expr).render(**kwargs)))
    return rendered_string
