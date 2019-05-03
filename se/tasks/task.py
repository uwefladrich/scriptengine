import shutil

from se.helpers import render_string_recursive


class Task(object):

    def __init__(self, dictionary, *required_args):
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
                raise UnboundLocalError(self.__class__.__name__+' is missing the "'+str(arg)+'" argument')

    def __repr__(self):
        return '{}({})'.format(self. __class__.__name__, self.__dict__)

    def run(self, **config):
        raise NotImplementedError('Task.run() method called, which is an abstract base class method')


class Echo(Task):

    def __init__(self, dict):
        super(Echo, self).__init__(dict, 'msg')

    def __str__(self):
        return 'Echo: {}'.format(self.msg)

    def run(self, *, dryrun=False, **config):
        if dryrun:
            print(render_string_recursive(str(self), **config))
        else:
            print('{}'.format(render_string_recursive(self.msg, **config)))


class Copy(Task):

    def __init__(self, dict):
        super(Copy, self).__init__(dict, 'src', 'dst')

    def __str__(self):
        return 'Copy: {} --> {}'.format(self.src, self.dst)

    def run(self, *, dryrun=False, **config):
        if dryrun:
            print(render_string_recursive(str(self), **config))
        else:
            shutil.copy(render_string_recursive(self.src, **config), render_string_recursive(self.dst, **config))


class Link(Task):

    def __init__(self, dict):
        super(Link, self).__init__(dict, 'src', 'dst')

    def __str__(self):
        return 'Link: {} --> {}'.format(self.src, self.dst)

    def run(self):
        print(self)


class Command(Task):

    def __init__(self, dict):
        super(Command, self).__init__(dict, 'name')

        if 'args' not in self.__dict__:
            self.args = []
        else:
            # Assert args is a list
            pass

    def __str__(self):
        return 'Running command "{}" with argument list "{}"'.format(self.name, self.args)

    def run(self):
        print(self)
