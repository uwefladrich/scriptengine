import jinja2

from se.tasks import Task
from se.helpers import render_string


class Template(Task):

    def __init__(self, dict):
        super(Template, self).__init__(__name__, dict, 'src', 'dst')
        self.log_debug('Creating "{}"'.format(dict))

    def __str__(self):
        return 'Template: {} --> {}'.format(self.src, self.dst)

    def run(self, *, dryrun=False, **config):
        self.log_info('{} --> {}'.format(render_string(self.src, **config),
                                         render_string(self.dst, **config)))
        if dryrun:
            print(render_string(str(self), **config))
        else:
            template_loader = jinja2.FileSystemLoader(searchpath=['./', './templates'])
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template(render_string(self.src, **config))
            output_text = render_string(template.render(**config), **config)

            with open(render_string(self.dst, **config), 'w') as output_file:
                output_file.write(output_text + '\n')
        return None
