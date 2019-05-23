import jinja2

from se.tasks import Task
from se.helpers import render_string_recursive


class Template(Task):

    def __init__(self, dict):
        super(Template, self).__init__(__name__, dict, 'src', 'dst')
        self.log.debug('Creating "{}"'.format(dict))

    def __str__(self):
        return 'Template: {} --> {}'.format(self.src, self.dst)

    def run(self, *, dryrun=False, **config):
        self.log.info('{} --> {}'.format(render_string_recursive(self.src, **config),
                                         render_string_recursive(self.dst, **config)))
        if dryrun:
            print(render_string_recursive(str(self), **config))
        else:
            template_loader = jinja2.FileSystemLoader(searchpath=['./', './templates'])
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template(render_string_recursive(self.src, **config))
            output_text = render_string_recursive(template.render(**config), **config)

            with open(render_string_recursive(self.dst, **config), 'w') as output_file:
                output_file.write(output_text + '\n')
        return None
