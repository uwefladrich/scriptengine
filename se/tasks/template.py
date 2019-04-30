import jinja2

from se.tasks import Task
from se.helpers import render_string_recursive


class Template(Task):

    def __init__(self, dict):
        super(Template, self).__init__(dict, 'src', 'dst')

    def __str__(self):
        return 'Template: {} --> {}'.format(self.src, self.dst)

    def run(self, *, dryrun=False, **kwargs):
        if dryrun:
            print(render_string_recursive(str(self), **kwargs))
        else:
            template_loader = jinja2.FileSystemLoader(searchpath=['./', './templates'])
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template(render_string_recursive(self.src, **kwargs))
            output_text = template.render(**kwargs)

            with open(render_string_recursive(self.dst, **kwargs), 'w') as output_file:
                output_file.write(output_text + '\n')
