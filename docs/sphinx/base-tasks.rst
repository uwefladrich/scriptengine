The base task package
=====================


Change dir task
---------------
Usage::

    base.chdir:
        path: <PATH>

Example::

    base.chdir:
        path: "{{se.cli.pwd}}"


Command task
------------
Executes an external command, with optional arguments.

Usage::

    - base.command:
        name: <COMMAND_NAME>
        args: <LIST_OF_ARGS>  # optional
        cwd: <PATH>  # optional
        stdout: [true|false|<STRING>]  # optional
        stderr: [true|false|<STRING>]  # optional
        ignore_error: [true|false]  # optional

When ``cwd`` (current work directory) is specified, the command is executed in
the given directory::

    - base.command:
        name: ls
        args: [-l]
        cwd: /tmp

When the ``stdout`` is given, it can be eiter a true value (e.g. ``true``,
``True``, ``Yes``, ``ON`` in YAML), a false value, or a string that makes for a
valid name in the ScriptEngine context. If ``stdout`` is set to true (the
default), then the standard output of the command is printed as log messages
(on the info level). When ``stdout`` is false, the standard output of the
command is ignored.

When ``stdout`` is a name, the standard output of the command is stored, under
that name, in the ScriptEngine context, for example::

    - base.command:
        name: echo
        args: [ Hello, World! ]
        stdout: message
    - base.echo:
        msg: "Command returned: {{message}}"

Note that the standard output is always returned as a list of lines, even if
there is only one line (as in the example above). This is often desired, for
example when using the command output in a loop. However, if one wanted to
extract the first (and only) line in the example above, Jinja2 syntax could be
used::

    - echo:
        msg: "Command returned: {{message|first}}"

The ``stderr`` argument works exactly as ``stdout``, but for standard error
output.

If the command returns a non-zero exit code, ScriptEngine writes the exit code
as log message (on the error level) and stops.  However, if ``ignore_error`` is
set to true and the command returns a non-zero exit code, the exit code of the
command is logged at the warning level instead and ScriptEngine continues. The
default value for ``ignore_error`` is false.


Context task
------------
Stores or updates data (one or more, possibly nested, pairs of names and values)
in the ScriptEngine context.

Usage::

    base.context:
        <NAME>: <VALUE>
        [...]

Example::

    base.context:
        planet: Earth
        some_countries:
            - Norway
            - Sweden
            - Finnland
            - Danmark
        number: 4

The arguments of ``base.context`` will be *merged* into the ScriptEngine
context. This means that data can be added to existing data structures, such as
lists or dictionaries::

    - base.context:
        mylist:
            - one
            - two
    # mylist is ['one', 'two']
    - base.context:
        mylist:
            - 3
            - 4
    # mylist is now ['one', 'two', 3, 4]

In the case of conflicts, the arguments of ``base.context`` will overwrite the
current values in the ScriptEngine context. This can be used to clean data::

    - base.context:
        mylist:
            - one
            - two
    # mylist is ['one', 'two']
    - base.context:
        mylist: null  # "remove" the value if mylist
    - base.context:
        mylist:
            - 3
            - 4
    # mylist is now [3, 4]


Context.from task
-----------------
This is an extension of ``base.context``. It updates the ScriptEngine context in
the same way, but it allows to "read" the context update from another source
instead of explicitly specifying the name-value pairs as task arguments. In
particular, ``base.context.from`` accepts one of two arguments, ``dict`` or
``file``. The arguments are mutual exclusive::

    base.context.from:
        # exactly one of the two arguments:
        dict: <DICTIONARY>  # optional, mutual exclusive
        file: <FILE_NAME>  # optional, mutual exclusive


If given the ``dict`` argument, the context update is specified by the argument
value, which must be a dictionary. This may sound rather similar to the standard
``base.context``, but it allows greater flexibility because the argument value
can be taken from the context itself. For example, one could implement
overwriteable default settings using this feature::

    # Let the user set preferred values
    - base.context:
        user_config:
            foo: 5
    # [... later (could be in another script) ...]
    # Set default values
    - base.context:
        foo: 1
        bar: 2
    # Overwrite defaults with user preferences
    - base.context.from:
        dict: "{{ user_config  }}"
    # result: foo==5, bar==2

The ``file`` argument of ``base.context.from`` can be used to read context
values from a YAML file::

    # data.yml
    foo: 4
    bar: 5

    # script.yml
    - base.context.from:
        file: data.yml

When running the scripte with ``se script.yml``, the context will contain
``foo==4`` and ``bar==5``, provided that the file ``data.yml`` can be found in
the current directory.

The only supported file format for the time being is YAML. The content of the
file must be a, possibly nested, dictionary (i.e. single values or lists are not
allowed).


Copy task
---------
This task copies the file or directory given by ``src`` to ``dst``. If ``src``
is a file and ``dst`` is a directory, the ``src`` file is copied into the
``dst/`` directory. If ``src`` is a directory, ``dst`` must be a directory as
well and ``src`` is copied recursively into ``dst/``. When a directory is
copied, symbolic links are preserved.

Usage::

    - base.copy:
        src: <PATH>
        dst: <PATH>
        ignore_not_found: <BOOL>  # optional

When copying a file and the ``dst`` exists already, it is overwritten and a
waring is issued. Copying a directory when ``dst`` already exists results in
an error. An error occurs if ``src`` does not exist, unless ``ignore_not_found``
is ``True``.


Echo task
---------
Displays a customised message.

Usage::

    - base.echo:
        msg: <MESSAGE>

Example::

    - base.context:
        planet: Earth
    - base.echo:
        msg: "Hello, {{planet}}!"


Exit task
---------
Requests ScriptEngine to stop, optionally displaying a customised message.

Usage::

    - base.exit:
        msg: <MESSAGE>  # optional


Find task
---------
Usage::

    base.find:
        path: <PATH>
        pattern: <SEARCH_PATTERN>  # optional
        type: <FILE_OR_DIR>  # optional


Getenv task
-----------
Reads one or more environment variables and stores the values in the
ScriptEngine context.

Usage::

    - base.getenv:
        <CONTEXT_PARAMETER>: <ENV_VAR_NAME>
        [...]

Example::

    - base.getenv:
        name: USER
        home: HOME
    - base.echo:
        msg: "I am {{name}} and {{home}} is my castle."

.. warning::
   Only simple, non-nested context parameters can be used in ``base.getenv``!


Setenv task
-----------
Sets one or more environment variables from values of the ScriptEngine context.

Usage::

    - base.setenv:
        <ENV_VAR_NAME>: <CONTEXT_PARAMETER>
        [...]

The following example::

    - base.context:
        libs: /path/to/libraries
    - base.setenv:
        LD_LIBRARY_PATH:  "{{libs}}"
        FOO: 1
        bar: two

will set the environment variables ``$LD_LIBRARY_PATH`` to
``"/path/to/libraries"``, ``$FOO`` to ``"1"`` and ``$bar`` to ``"two"``.

.. note::
   Environment variables are always strings! Thus, all values are converted to
   strings before they are assigned. In the above example, the number ``1`` is
   converted to the string ``"1"`` before it is assigned to the environment
   variable ``$FOO``.

.. warning::
   Only simple, non-nested context parameters can be used in ``base.setenv``!


Include task
------------
Usage::

    - base.include:
        src: <PATH>
        ignore_not_found: [true|false]  # optional

Includes and runs a ScriptEngine script given by the ``src`` argument, which
must be a relative path. The script is search relative to the current working
directory at the moment the include task is run, the original working directory
when the ``se`` command was run, or any of the directories that the scripts
given to the ``se`` command were in.

If ``ingore_not_found`` is ``True``, a warning is written in case the include
script is not found. If it is ``False`` (the default) an error is raised.


Link task
---------
Creates a symbolic link with name given by ``dst``, which is pointing to the
path given by ``src``.

Usage::

    base.link:
        src: <PATH>
        dst: <PATH>

When the ``dst`` path (i.e. the link target) does not exist, the link is still
created and a warning is issued.


Make directory task
-------------------
Creates a new directory at the given ``path``.

Usage::

    base.make_dir:
        path: <PATH>

If ``path`` already exists, an info message is displayed (no warning or error).
When ``path`` is a file or symbolic link, an error occurs.


Move task
---------
Usage::

    base.move:
        src: <PATH>
        dst: <PATH>


Remove task
-----------
Removes a file, link, or directory. Directories are recursively deleted,
effectively removing all files and subdirectories that it contains.

Usage::

    base.remove:
        path: <PATH>

When ``path`` does not exist, an info message is displayed (no warning or
error).


Task timer task
---------------
Usage::

    base.task_timer:
        mode: <TIMING_MODE>
        logging: <LOGLEVEL>  # optional

where::

    TIMING_MODE is one of
        False:       Timing is switched off.
        'basic':     Each task is timed, log messages are written according to
                     'logging' argument.
        'classes':   As for 'basic', plus times are accumulated for task
                     classes.
        'instances': As for 'classes', plus times are accumulated for each
                     individual task instance.

and::

    LOGLEVEL is one of
        False:   No time logging after each task. Does not affect statistic
                 collection.
        'info':  Logging to the info logger.
        'debug': Logging to the debug logger


Template task
-------------
Runs the template file given by ``src`` through the `Jinja2 Template Engine
<http://jinja.pocoo.org/>`_ and saves the result as a file at ``dst``.

Usage::

    base.template:
        src: <PATH>
        dst: <PATH>
        executable: [true|false]  # optional

ScriptEngine searches for the template file (``src``) in the following
directories, in the order given:

#. ``.``
#. ``./templates``
#. ``{{se.cli.cwd}}``
#. ``{{se.cli.cwd}}/templates``

where ``.`` is the current directory at the time when the ``template`` task
is executed and ``{{se.cli.cwd}}`` is the original working directory, the
working directory at the time when the ScriptEngine command line tool was
called.

The ScriptEngine context is passed to the Jinja2 template engine when the
template is rendered, which means that all context parameters can be referred to
in the template.

If the ``executable`` argument is true (the default being false), the
destination file will get executable permissions. The setting of permissions
will respect the user's umask.


Time task
---------
Usage::

    base.time:
        set: <CONTEXT_VARIABLE>
        since: <DATETIME>  # optional
