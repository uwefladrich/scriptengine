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
        """ Run all tasks of a job, subject to it's when clause and repeated
            for each loop item
        """
        when = self.when or 'true'
        assert (type(when) is str), 'Tasks "when" argument is not a string'

        loop = self.loop or [None]
        assert (type(loop) is list), 'Tasks "loop" argument is not a list'

        if eval_when_clause(when, **kwargs):
            for item in loop:
                for task in self.tasks:
                    task.run(dryrun=dryrun, item=item, **kwargs)
