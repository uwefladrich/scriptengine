from jinja2 import Template
from distutils.util import strtobool


def render_string(string, **config):
    return Template(string).render(**config)


def render_string_recursive(string, **config):
    prev = string
    while True:
        curr = render_string(prev, **config)
        if curr != prev:
            prev = curr
        else:
            return curr


def eval_when_clause(string, **config):
    clause = ('{% if '
              + render_string_recursive(string, **config)
              + ' %}1{% else %}0{% endif %}')
    return bool(strtobool(render_string(clause, **config)))
