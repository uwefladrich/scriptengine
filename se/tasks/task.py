import logging

class Task(object):
    """Base class for all tasks in ScriptEngine.

    This class provides (parts of) the initialisation of task objects, set-up
    of the logging mechanism, and a custom __repr__ method.

    To make use of this abstract base class, the following steps are usually
    needed:
    - derive a subclass
    - extend the __init__() method by overwriting and calling Task.__init__()
    - overwrite the run() method

    For initialising a subclass object, call the __init__ method via super()
    and provide the names (as strings) of the required attributes (see example
    below). All key-value pairs present in the 'dictionary' argument are made
    available as self.key attributes in the task object. The initialisation
    checks that at least the attributes present in '*required_attributes' are
    present when the object is created.

    Every subclass of Task must at least overwrite the run() method, which is
    where the actual task work is done! The run method can access the key-value
    pairs present at initialisation time as attributes of 'self'.

    Usually, the attributes need to be rendered by using render_string() from
    se.helpers, e.g.

    rendered_attr = render_string(self.attr, **kwargs)

    Here, **kwargs provides the configuration context for the task execution.

    Example:

        Create a Copy class of tasks that copy a file from a source to a
        destination path.

        class Copy(Task):

            def __init__(self, dictionary):
                super(Copy, self).__init__(__name__, 'src', 'dst')

            def run(self, **kwargs):
                shutil.copy(render_string(self.src, **kwargs),
                            render_string(self.dst, **kwargs))

    The derived classes should make use of the logging facility that is set up
    in the base class. This is done by the log_debug, log_info, log_warning,
    and log_error methods, e.g.

        def run(self, **kwargs):
            self.log_info('{} --> {}'.format(render_string(self.src),
                                             render_string(self.dst)))
            shutil.copy(render_string(self.src, **kwargs),
                        render_string(self.dst, **kwargs))

    Note that the name of the task object is automatically added.

    The run() method must return either None or a dictionary. If a dictionary
    is returned, it's key-value pairs are added to the configuration context.
    """

    def __init__(self, logger_name, dictionary, *required_attributes):
        """Creating object attributes from a dictionary and set up logging.

        Args:
            logger_name (str): The name of the logger which this task will log
                to. Usually, this should be the __name__ of the module where
                the task class is defined.
            dictionary (dict): The dictionary that defines this task. All keys
                in the dict will be converted into object attributes. Note that
                'run' is not allowed as a key (to avoid conflict with the run()
                method).
            required_attributes: Strings that define a list of attributes that
                must be present when creating an object of this task class.

        Attributes:
            <attr>: All keys provided in the dictionary argument are converted
                to object attributes
        """
        try:
            # Make sure that 'run' is not a dictionary key, it's reserved for the run() method!
            if 'run' in dictionary:
                raise RuntimeError('Reserved identifier "run" used when creating task')
            # Add all key/value pairs as instance attributes
            self.__dict__.update(dictionary)
        except TypeError:
            raise TypeError('Tasks must be created from a dictionary')
        # Make sure all required arguments are present
        for key in required_attributes:
            if key not in self.__dict__:
                raise UnboundLocalError('{} is missing the {} argument'.format(self.__class__.__name__, str(key)))
        # Associate this task with the given logger name
        self.__log = logging.getLogger(logger_name)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.__dict__)

    def run(self, **kwargs):
        """Abstract run function that can't be called directly.

        The derived classes must overwrite this function!

        Args:
            kwargs: name=value pairs that provide the context for rendering
                any attributes.

        Returns:
            dict or None: If the task wants to add/update the
                configuration, a dict is returned. None otherwise.
        """
        raise NotImplementedError('Task.run() method called, which is an abstract base class method')

    def log_debug(self, msg):
        self.__log.debug(msg)

    def log_info(self, msg):
        self.__log.info(msg)

    def log_warning(self, msg):
        self.__log.warning(msg)

    def log_error(self, msg):
        self.__log.error(msg)
