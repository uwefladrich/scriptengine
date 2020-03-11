"""Template task for ScriptEngine."""

import os
from itertools import chain
import jinja2

from scriptengine.tasks import Task
from scriptengine.jinja import render as j2render
from scriptengine.jinja import filters as j2filters


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
        src_path = j2render(self.src, context)
        dst_path = j2render(self.dst, context)
        self.log_info(f"Render {src_path} --> {dst_path}")

        # The template search path:
        #   1. .
        #   2. ./templates
        #   3. <ocwd>
        #   4. <ocwd>/templates
        # where <ocwd> is the original working directory at the time when the se script was called
        search_path = [ '.', 'templates' ]
        if "_se_ocwd" in context:
            search_path.extend([context["_se_ocwd"],
                                os.path.join(context["_se_ocwd"], "templates")])
        self.log_debug(f"Search path for template: {search_path}")

        loader = jinja2.FileSystemLoader(search_path)
        environment = jinja2.Environment(loader=loader)
        for name, function in j2filters().items():
            environment.filters[name] = function
        template = environment.get_template(src_path)
        output_text = j2render(template.render(context), context)

        with open(dst_path, "w") as output_file:
            output_file.write(f"{output_text}\n")
