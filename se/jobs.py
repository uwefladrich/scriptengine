import ast

from deepmerge import always_merger

from se.helpers import eval_when_clause, render_string_recursive


class Job(object):
    """A Job is ...
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
        str_repr  = 'Task list:\n  '
        str_repr += '\n  '.join([str(task) for task in self.tasks])
        str_repr += '\nWhen: {}'.format(self.when)
        str_repr += '\nLoop: {}'.format(self.loop)
        str_repr += '\nContext: {}'.format(self.context)
        return str_repr

    def __repr__(self):
        return 'Job: {} {}'.format(str([t.__class__.__name__ for t in self.tasks]), self.loop or '')

    def append(self, tasks):
        """ Append a single task or a list of tasks to a job
        """
        self.tasks.extend(tasks if type(tasks) is list else [tasks])

    def run(self, **config):
        """Run all tasks/jobs of this job.
           If this job has a where clause, run only if it evaluates to true. If
           this job has a list to loop over, run the tasks/jobs repeatedly for
           each loop item.
        """
        if self.when is None or eval_when_clause(self.when, **config):
            non_loop = object()
            config_updates = {}
            if type(self.loop) is str:
                try:
                    self.loop = ast.literal_eval(
                                    render_string_recursive(self.loop, **config))
                except ValueError:
                    raise RuntimeError('Found invalid loop expression: {}'.format(self.loop))
            for item in self.loop or [non_loop]:
                for task in self.tasks:
                    if item is non_loop:
                        cfg = task.run(**{**config, **config_updates})
                    else:
                        cfg = task.run(item=item, **{**config, **config_updates})
                    if cfg is not None:
                        always_merger.merge(config_updates, cfg)
            if config_updates is not {}:
                return config_updates
        return None
