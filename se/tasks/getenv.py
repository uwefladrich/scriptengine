import logging
import os

from se.tasks import Task
from se.helpers import render_string_recursive

log = logging.getLogger(__name__)

class Getenv(Task):

    def __init__(self, dict):
        super(Getenv, self).__init__(dict, 'name', 'set_cfg')
        log.debug('Creating "{}"'.format(dict))

    def __str__(self):
        return 'Get environment variable "{}" and set "{}" config'.format(self.name, self.set_cfg)

    def run(self, *, dryrun=False, **config):
        log.info('{} --> {}'.format(render_string_recursive(self.name, **config),
                                    render_string_recursive(self.set_cfg, **config)))
        if dryrun:
            print(render_string_recursive(str(self), **config))
            return None

        env = os.environ.get(render_string_recursive(self.name, **config))
        if env:
            return {render_string_recursive(self.set_cfg, **config): env}
        else:
            return None
