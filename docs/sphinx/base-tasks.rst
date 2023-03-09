The base task package
=====================
The ScriptEngine **base** task package collects essential tasks that are
commonly needed to write scripts. The base task package is pre-installed in
ScriptEngine and any task within the ``base.*`` namespace can be used without
further installation or setup. Many useful ScriptEngine scripts can be written
with just the base task package.

The base task package contains the following tasks, described in more detail below::

    base.echo, base.chdir, base.command, base.context, base.context.from,
    base.copy, base.exit, base.find, base.getenv, base.include, base.link,
    base.make_dir, base.move, base.remove, base.setenv, base.task_timer,
    base.template, base.time


``base.echo``
-------------
This is a very basic task that can be used to write customised messages::

    base.echo:
        msg: <MESSAGE>

for example::

    base.echo:
        msg: Hello, world!

or, provided that ``planet`` is set in the context (`base.context`_)::

    base.echo:
        msg: "Hello, {{ planet }}!"


Working with the SE context
---------------------------

``base.context``
^^^^^^^^^^^^^^^^
Stores or updates data (one or more, possibly nested, pairs of names and values)
in the ScriptEngine context::

    base.context:
        <NAME>: <VALUE>
        [...]

For example::

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


``base.context.from``
^^^^^^^^^^^^^^^^^^^^^
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

When running the script with ``se script.yml``, the context will contain
``foo==4`` and ``bar==5``, provided that the file ``data.yml`` can be found in
the current directory.

The only supported file format for the time being is YAML. The content of the
file must be a, possibly nested, dictionary (i.e. single values or lists are not
allowed).


Control flow
------------

``base.include``
^^^^^^^^^^^^^^^^
Reads and executes another ScriptEngine script. This is done *if* (see
:ref:`scripts:Conditionals`) and *when* the ``base.include`` task is executed::

    base.include:
        src: <PATH>
        ignore_not_found: <true or false>  # optional, default false

The script to be included is given by the ``src`` argument, which must be a path
relative to

- the current working directory at the moment ``base.include`` is
  run,
- the original working directory when the ``se`` command was run, or
- any of the directories that the scripts given to the ``se`` command were in.

If ``ignore_not_found`` is ``true``, only a warning is written in case the
include script is not found. If it is ``false`` (the default) an error is
raised in this case.


``base.command``
^^^^^^^^^^^^^^^^
Executes an external command, with optional arguments::

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

When the ``stdout`` is given, it can be either true, false, or a string that
makes for a valid name in the ScriptEngine context. If ``stdout`` is set to true
(the default), then the standard output of the command is printed as log
messages on the INFO level. When ``stdout`` is false, the standard output of the
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

.. note::
    When tasks update the ScriptEngine context, the changes are always *merged*
    (see `base.context`_). This implies, among other things, that list items are
    *appended* if the list is already defined in the context. This mechanism
    applies also to ``base.command`` and consequently output lines are appended
    to the context variable if it already exists.

The ``stderr`` argument works exactly as ``stdout``, but for standard error
output.

If the command returns a non-zero exit code, ScriptEngine writes the exit code
as log message (on the ERROR level) and stops with an error.  However, if
``ignore_error`` is true and the command returns a non-zero exit code, the exit
code of the command is logged at the WARNING level instead and ScriptEngine
continues. The default value for ``ignore_error`` is false.


``base.exit``
^^^^^^^^^^^^^
Requests ScriptEngine to stop, optionally displaying a customised message::

    - base.exit:
        msg: <MESSAGE>  # optional

If the ``msg`` argument is not given, a default message is printed.


Shell environment
-----------------

``base.chdir``
^^^^^^^^^^^^^^
This task changes the current working directory::

    base.chdir:
        path: <PATH>

for example::

    - base.getenv:
        home: HOME
    - base.chdir:
        path: "{{ home }}"


``base.getenv``
^^^^^^^^^^^^^^^
Reads one or more environment variables and stores the values in the
ScriptEngine context::

    - base.getenv:
        <CONTEXT_PARAMETER>: <ENV_VAR_NAME>
        [...]

for example::

    - base.getenv:
        name: USER
        home: HOME
    - base.echo:
        msg: "I am {{ name }} and {{ home }} is my castle."

When a requested environment variable does not exist, a warning is given and no
corresponding context changes are made.

.. warning::
   Only simple, non-nested context parameters (without dots) can be used in
   ``base.getenv``


``base.setenv``
^^^^^^^^^^^^^^^
Sets one or more environment variables from values of the ScriptEngine context::

    - base.setenv:
        <ENV_VAR_NAME>: <CONTEXT_PARAMETER>
        [...]

The following example::

    - base.context:
        libs: /path/to/libraries
    - base.setenv:
        LD_LIBRARY_PATH:  "{{ libs }}"
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
   Only simple, non-nested context parameters can be used in ``base.setenv``


Basic file operations
---------------------

The ScriptEngine base task package provides tasks to create, copy/move/link and
remove files and directories, as described in detail below in this section.

Whenever it makes sense, the tasks will accept as their argument values single
file or directory names, as well as YAML lists of such. Furthermore, instead of
full names, also Unix shell wildcard expressions are accepted.


``base.make_dir``
^^^^^^^^^^^^^^^^^
Creates a new directory at the given ``path``::

    base.make_dir:
        path: <PATH>

If ``path`` already exists, an info message is displayed (no warning or error).
This task creates parent directories as needed. An error is raised when
``path`` is a file or symbolic link.

A list of names is accepted for the ``path`` argument.


``base.copy``
^^^^^^^^^^^^^
This task copies the file or directory given by ``src`` to ``dst``::

    - base.copy:
        src: <PATH>
        dst: <PATH>
        ignore_not_found: <true or false>  # optional, default false

If ``src`` is a file and ``dst`` is a directory, the ``src`` file is copied into
the ``dst/`` directory. If ``src`` is a directory, ``dst`` must be a directory
as well and ``src`` is copied recursively into ``dst``. When a directory is
copied, symbolic links are preserved.

When copying a file and the ``dst`` exists already, it is overwritten and a
warning is issued. Copying a directory when ``dst`` already exists results in
an error. An error occurs if ``src`` does not exist, unless ``ignore_not_found``
is ``true``.

A list of names or wildcard expressions is accepted for the ``src`` argument,
provided that ``dst`` is a directory.


``base.link``
^^^^^^^^^^^^^
Creates a symbolic link with name given by ``link``, which is pointing to the
path given by ``target``::

    base.link:
        target: <PATH>
        link: <PATH>

When the ``target`` does not exist, the link is still created and a warning is
issued.

When ``link`` is a directory, a symbolic link with the same base name as
``target`` is created within the ``link`` directory, pointing to ``target``.

A list of names or wildcard expressions is accepted for the ``target`` argument,
provided that ``link`` is a directory. A symbolic link for each ``target`` is
created in that case in the ``link`` directory.

.. warning::
    In ScriptEngine versions up to 0.13.1 the arguments of ``base.link`` were
    named ``src`` (now ``target``) and ``dst`` (now ``link``). The use of these
    argument names is deprecated and will be invalid in future versions of
    ScriptEngine.
    The use of directories for ``dst`` or lists and wildcards for ``src`` was
    not available in those versions.


``base.move``
^^^^^^^^^^^^^
Moves files or directories (the latter recursively) from ``src`` to ``dst``::

    base.move:
        src: <PATH>
        dst: <PATH>
        ignore_not_found: <true or false>  # optional, default false

If ``dst`` is a directory, ``src`` is moved *into* ``dst``. If ``src`` does not
exists, an error occurs unless ``ignore_not_found`` is true.

Provided that ``dst`` is a directory, ``src`` may be a list or wildcard
expression.


``base.remove``
^^^^^^^^^^^^^^^
Removes a file, link, or directory::

    base.remove:
        path: <PATH>
        ignore_not_found: <true or false>  # optional, default false

Directories are recursively deleted, effectively removing all files and
subdirectories that it contains. When ``path`` does not exist, an error occurs,
unless ``ignore_not_found`` is ``true``.

A list of names or wildcard expressions is accepted for ``path``.


Other file operations
---------------------

``base.template``
^^^^^^^^^^^^^^^^^
Runs the template file given by ``src`` through the `Jinja2 Template Engine
<http://jinja.pocoo.org/>`_ and saves the result as a file at ``dst``::

    base.template:
        src: <PATH>
        dst: <PATH>
        executable: [true|false]  # optional

ScriptEngine searches for the template file (``src``) in the following
directories, in the order given:

#. ``.``
#. ``./templates``
#. ``{{ se.cli.cwd }}``
#. ``{{ se.cli.cwd }}/templates``

where ``.`` is the current directory at the time when the ``template`` task is
executed and ``{{se.cli.cwd}}`` is the original working directory, the working
directory at the time when the ScriptEngine command line tool was called.

The ScriptEngine context is passed to the Jinja2 template engine when the
template is rendered, which means that all context parameters can be referred to
in the template.

If the ``executable`` argument is true (the default being false), the
destination file will get executable permissions. The setting of permissions
will respect the user's umask.


``base.find``
^^^^^^^^^^^^^
This task can be used to find files or directories in the file system::

    base.find:
        path: <PATH>
        pattern: <SEARCH_PATTERN>  # optional, default "*"
        type: <FILE_OR_DIR>  # optional, default "file"
        depth: <NUMBER>  # optional, default -1
        set: <CONTEXT_PARAMETER>  # optional, default "result"

Files and directories are searched starting at ``path`` and descending at most
``depth`` levels down the directory hierarchy. If ``depth`` is less than zero,
no limit is used for the search. Files and directories are matched against the
Unix shell-style wildcards ``pattern``, which may include:

.. code-block:: shell

    *       matches everything
    ?       matches any single character
    [seq]   matches any character in seq
    [!seq]  matches any character not in seq

If ``type`` is ``file`` (default) or ``dir``, then ``base.find`` will search for
files or directories, respectively.

.. note::

    ``base.find`` supports Unix shell-type wildcards, not regular expressions.


Timing
------

``base.time``
^^^^^^^^^^^^^
This task can be used to measure absolute or elapsed time in ScriptEngine
scripts::

    base.time:
        set: <CONTEXT_NAME>
        since: <DATETIME>  # optional

The ``set`` argument specifies a name under which the time is stored in the
context. Only simple names, without dots, may be used.

If the ``since`` argument is used, it must represent a ``datetime`` object and
the elapsed time since this reference is measured::

    - base.time:
        set: start
    - base.echo:
        msg: Hello, world!
    - base.time:
        set: elapsed_time
        since: "{{ start }}"


``base.task_timer``
^^^^^^^^^^^^^^^^^^^
This task can be used to control ScriptEngine's build-in timing feature. It is
used as::

    base.task_timer:
        mode: <TIMING_MODE>
        logging: <LOGLEVEL>  # optional

where::

    TIMING_MODE is one of
        false:       Timing is switched off.
        'basic':     Each task is timed, log messages are written according to
                     'logging' argument.
        'classes':   As for 'basic', plus times are accumulated for task
                     classes.
        'instances': As for 'classes', plus times are accumulated for each
                     individual task instance.

and::

    LOGLEVEL is one of
        false:   No time logging after each task
        'info':  Logging to the info logger
        'debug': Logging to the debug logger

.. note::
    Switching off logging (``LOGLEVEL: false``) does not affect the collection
    of timing data for the tasks.

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
