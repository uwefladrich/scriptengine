"""Template task for ScriptEngine."""

import jinja2

from se.tasks import Task
from se.helpers import render_string


class Template(Task):
    """Template task, renders a template with Jinja2 and writes result to file.

    The task needs a source (a Jinja2 template file) and a destination. It
    renders the template given the context passed in kwargs and writes the
    result to the destination file.

    Args:
        dictionary (dict): Must at least contain the following keys:
            - src: Source file name (a Jinja2 template)
            - dst: Destination file name
    """
    def __init__(self, dictionary):
        super().__init__(__name__, dictionary, 'src', 'dst')

    def __str__(self):
        return f'Template: {self.src} --> {self.dst}'

    def run(self, **kwargs):
        self.log_info(f'{render_string(self.src, **kwargs)} '
                      f'--> {render_string(self.dst, **kwargs)}')
        if getattr(kwargs, 'dryrun', False):
            print(render_string(str(self), **kwargs))
        else:
            template_loader = jinja2.FileSystemLoader(searchpath=['./', './templates'])
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template(render_string(self.src, **kwargs))
            output_text = render_string(template.render(**kwargs), **kwargs)

            with open(render_string(self.dst, **kwargs), 'w') as output_file:
                output_file.write(f'{output_text}\n')
