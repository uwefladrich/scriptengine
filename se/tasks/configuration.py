import jinja2

from se.tasks import Task
from se.helpers import render_string


class Configuration(Task):

    def __init__(self, dict):
        super(Configuration, self).__init__(__name__, dict)
        self.log_debug('Creating "{}"'.format(self.__dict__))

    def __str__(self):
        return 'Configuration: {}'.format(self.__dict__)

    def run(self, *, dryrun=False, **config):
        self.log_info('{}'.format(render_string(str(self.__dict__), **config)))
        if dryrun:
            print(render_string(str(self), **config))
        return self.__dict__
