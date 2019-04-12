import shutil

from se.helpers import render_string_recursive


class Task(object):

    def __init__(self, dict):
        # Reserved identifiers for functions that subclasses must implement
        _reserved_identifiers = {'run'}

        # Make sure only subclasses of Task are instantiated
        assert (self.__class__.__name__ is not 'Task'), \
               'Do not create Tasks directly, use subclasses!'

        # Make sure that the Task is created from a dictionary and that the
        # dictionary does not contain any of the reserved identifiers as a key
        try:
            assert (not dict.keys() & _reserved_identifiers), \
                   'Reserved identifiers used when creating {} task: {}'.format(self.__class__.__name__,
                                                                    dict.keys() & _reserved_identifiers)
        except AttributeError:
            raise TypeError('{} task must be created from dictionary'.format(self.__class__.__name__))

        # Add all key/value pairs as instance members
        self.__dict__.update(dict)

    def __repr__(self):
        return '{}({})'.format(self. __class__.__name__, self.__dict__)


class Copy(Task):

    def __init__(self, dict):
        super(Copy, self).__init__(dict)
        assert ('src' in self.__dict__), 'Copy task needs a "src" attribute'
        assert ('dst' in self.__dict__), 'Copy task needs a "dst" attribute'

    def __str__(self):
        return 'Copy: {} --> {}'.format(self.src, self.dst)

    def run(self, *, dryrun=False, **kwargs):
        if dryrun:
            print(render_string_recursive(str(self), **kwargs))
        else:
            shutil.copy(render_string_recursive(self.src, **kwargs), render_string_recursive(self.dst, **kwargs))


class Link(Task):

    def __init__(self, dict):
        super(Link, self).__init__(dict)
        assert ('src' in self.__dict__), 'Link task needs a "src" attribute'
        assert ('dst' in self.__dict__), 'Link task needs a "dst" attribute'

    def __str__(self):
        return 'Link: {} --> {}'.format(self.src, self.dst)

    def run(self):
        print(self)


class Command(Task):

    def __init__(self, dict):
        super(Command, self).__init__(dict)
        assert ('name' in self.__dict__), 'Command task needs a "name" attribute'

        if 'args' not in self.__dict__:
            self.args = []
        else:
            # Assert args is a list
            pass

    def __str__(self):
        return 'Running command "{}" with argument list "{}"'.format(self.name, self.args)

    def run(self):
        print(self)
