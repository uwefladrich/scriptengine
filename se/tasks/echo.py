from se.tasks import Task
from se.helpers import render_string_recursive


class Echo(Task):

    def __init__(self, dict):
        super(Echo, self).__init__(dict, 'msg')

    def __str__(self):
        return 'Echo: {}'.format(self.msg)

    def run(self, *, dryrun=False, **kwargs):
        if dryrun:
            print(render_string_recursive(str(self), **kwargs))
        else:
            print('{}'.format(render_string_recursive(self.msg, **kwargs)))
