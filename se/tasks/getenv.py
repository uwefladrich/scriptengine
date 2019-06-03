import os

from se.tasks import Task
from se.helpers import render_string


class Getenv(Task):

    def __init__(self, dict):
        super(Getenv, self).__init__(__name__, dict, 'name', 'set_cfg')
        self.log_debug('Creating "{}"'.format(dict))

    def __str__(self):
        return 'Get environment variable "{}" and set "{}" config'.format(self.name, self.set_cfg)

    def run(self, *, dryrun=False, **config):
        self.log_info('{} --> {}'.format(render_string(self.name, **config),
                                         render_string(self.set_cfg, **config)))
        if dryrun:
            print(render_string(str(self), **config))
            return None

        env = os.environ.get(render_string(self.name, **config))
        if env:
            return {render_string(self.set_cfg, **config): env}
        else:
            return None
