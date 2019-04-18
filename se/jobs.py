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

    def run(self, *, dryrun=False, **kwargs):
        """Run all tasks/jobs of this job. If this job has a where clause, run
           only if it evaluates to true. If this job has a loop, run the
           tasks/jobs repeatedly for each loop item.
        """
        # If job has a when clause, evaluate it
        if self.when and not eval_when_clause(self.when, **kwargs):
            return

        if self.loop:
            if 'item' in kwargs:
                raise NotImplementedError('Nested loops are not yet supported')
            for item in self.loop:
                for task in self.tasks:
                    task.run(dryrun=dryrun, item=item, **kwargs)
        else:
            for task in self.tasks:
                task.run(dryrun=dryrun, **kwargs)
