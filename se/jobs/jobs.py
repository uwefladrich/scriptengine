""" ScriptEngine jobs.

Jobs are the second level (above tasks) work unit in ScriptEngine. Jobs are
made of tasks and may include loops, conditionals, and a context. Job lists can
be given to a ScriptEngine, for execution.
"""

import ast
import deepmerge

from se.helpers import render_string


class Job:
    """A Job is composed of
    - a (list of) tasks (see se.tasks for more information)
    - an optional 'loop' (a list of things to loop over)
    - an optional 'when' clause (a Jinja2 string)
    - an optional 'context' string
    - a run() method
    """

    def __init__(self, tasks=None, when=None, loop=None, context=None):
        # Initialise task list
        self.tasks = []
        if tasks:
            self.append(tasks)
        self.when = when
        self.loop = loop
        self.context = context

    def __str__(self):
        list_newline = "\n - "
        return (f'Task list:{list_newline}'
                f'{list_newline.join(map(str, self.tasks))}'
                f'When: {self.when!s}\n'
                f'Loop: {self.loop!s}\n'
                f'Context: {self.context!s}')

    def __repr__(self):
        return (f'Job: {[task.__class__.__name__ for task in self.tasks]!s}; '
                f'Loop: {self.loop}; '
                f'When: {self.when}; '
                f'Context: {self.context}')

    def append(self, tasks):
        """ Append a single task or a list of tasks to a job
        """
        self.tasks.extend(tasks if isinstance(tasks, list) else [tasks])

    def run(self, **config):
        """Run all tasks/jobs of this job.
           If this job has a where clause, run only if it evaluates to true. If
           this job has a list to loop over, run the tasks/jobs repeatedly for
           each loop item.
        """
        non_loop = object()
        config_updates = {}
        if self.when is None or render_string(self.when, boolean=True, **config):
            if isinstance(self.loop, str):
                try:
                    self.loop = ast.literal_eval(render_string(self.loop, **config))
                except (ValueError, SyntaxError):
                    raise RuntimeError('Invalid or undefined loop expression: {}'.format(self.loop))
            for item in self.loop or [non_loop]:
                for task in self.tasks:
                    if item is non_loop:
                        cfg = task.run(**{**config, **config_updates})
                    else:
                        cfg = task.run(item=item, **{**config, **config_updates})
                    if cfg is not None:
                        deepmerge.always_merger.merge(config_updates, cfg)
        return config_updates or None
