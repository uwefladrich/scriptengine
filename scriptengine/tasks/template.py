"""Template task for ScriptEngine."""

import os
from itertools import chain
import jinja2

from scriptengine.tasks import Task
from scriptengine.helpers import render_string


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
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["src", "dst"])

    def __str__(self):
        return f"Template: {self.src} --> {self.dst}"

    def run(self, context):
        src_path = render_string(self.src, context)
        dst_path = render_string(self.dst, context)
        self.log_info(f"Render {src_path} --> {dst_path}")

        # Build search path for template:
        #   1.) a "path" key in task spec
        search_path = render_string(getattr(self, "path", ""), context) or []
        #   2.) everything in the _se_filepath context
        search_path.extend(context.get("_se_filepath", []))
        #   3.) everything above, but with "/templates" appended
        search_path = list(chain.from_iterable(((p, os.path.join(p, "templates"))
                                                for p in search_path)))
        self.log_debug(f"Search path for template: {search_path}")

        loader = jinja2.FileSystemLoader(search_path)
        environment = jinja2.Environment(loader=loader)
        template = environment.get_template(src_path)
        output_text = render_string(template.render(context), context)

        with open(dst_path, "w") as output_file:
            output_file.write(f"{output_text}\n")
