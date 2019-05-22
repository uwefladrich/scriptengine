import logging
import jinja2

from se.tasks import Task
from se.helpers import render_string_recursive

log = logging.getLogger(__name__)

class Configuration(Task):

    def __init__(self, dict):
        super(Configuration, self).__init__(dict)
        log.debug('Creating "{}"'.format(self.__dict__))

    def __str__(self):
        return 'Configuration: {}'.format(self.__dict__)

    def run(self, *, dryrun=False, **config):
        log.info('{}'.format(render_string_recursive(str(self.__dict__), **config)))
        if dryrun:
            print(render_string_recursive(str(self), **config))
        return self.__dict__
