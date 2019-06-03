import logging

class Task(object):
    """ Base class for all tasks
    """
    def __init__(self, log_name, dictionary, *required_args):
        try:
            # Make sure that 'run' is not a dictionary key, it's reserved for the run() method!
            if 'run' in dictionary:
                raise RuntimeError('Reserved identifier "run" used when creating task')
            # Add all key/value pairs as instance members
            self.__dict__.update(dictionary)
        except TypeError:
            raise TypeError('Tasks must be created from a dictionary')
        # Make sure all required arguments are present
        for arg in required_args:
            if arg not in self.__dict__:
                raise UnboundLocalError('{} is missing the {} argument'.format(self.__class__.__name__, str(arg)))
        self.__log = logging.getLogger(log_name)

    def __repr__(self):
        return '{}({})'.format(self. __class__.__name__, self.__dict__)

    def run(self, **config):
        raise NotImplementedError('Task.run() method called, which is an abstract base class method')

    def log_info(self, msg):
        self.__log.info(msg)

    def log_debug(self, msg):
        self.__log.debug(msg)
