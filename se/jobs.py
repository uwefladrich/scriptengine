from se.helpers import eval_when_clause


class Job(object):
    """A Job is ...
    """
    def __init__(self, tasks=None, when=None, loop=None):
        # Initialise task list
        self.tasks = []
        if tasks:
           self.append(tasks)
        self.when = when
        self.loop = loop

    def __str__(self):
        str_repr  = 'Task list:\n  '
        str_repr += '\n  '.join([str(task) for task in self.tasks])
        str_repr += '\nWhen: {}'.format(self.when)
        str_repr += '\nLoop: {}'.format(self.loop)
        return str_repr

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
            for item in self.loop or [non_loop]:
                for task in self.tasks:
                    if item is non_loop:
                        cfg = task.run(**{**config, **config_updates})
                    else:
                        cfg = task.run(item=item, **{**config, **config_updates})
                    if cfg is not None:
                        config_updates.update(cfg)
            if config_updates is not {}:
                return config_updates
        return None
