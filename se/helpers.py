from jinja2 import Template
from distutils.util import strtobool


def read_yaml(path):
    pass


def read_eceinfo(path):
    pass


def render_string(string, **kwargs):
    return Template(string).render(**kwargs)


def render_string_recursive(string, **kwargs):
    prev = string
    while True:
        curr = render_string(prev, **kwargs)
        if curr != prev:
            prev = curr
        else:
            return curr


def eval_when_clause(string, **kwargs):
    clause = ('{% if '
              + render_string_recursive(string, **kwargs)
              + ' %}1{% else %}0{% endif %}')
    return bool(strtobool(render_string(clause, **kwargs)))
