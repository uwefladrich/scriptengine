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
Executes a command, with optional arguments.

Usage::

    - base.command:
        name: <COMMAND_NAME>
        args: <LIST_OF_ARGS> # optional
        cwd: <PATH> # optional
        stdout: <STRING> # optional
        ignore_error: [true|false] # optional

When ``cwd`` (current work directory) is specified, the command is executed in
the given directory::

    - base.command:
        name: ls
        args: [-l]
        cwd: /tmp

When the ``stdout`` is given, the standard output of the command is captured
and stored in the ScriptEngine context, for example::

    - base.command:
        name: echo
        args: [ Hello, World! ]
        stdout: message
    - base.echo:
        msg: "Command returned: {{message}}"

Note that the standard output is always returned as a list of lines, even if
there is only one line (as in the above example). This is often desired, for
example when using the command output in a loop. However, if one wanted to
extract the first (and only) line in the example above, Jinja2 syntax could be
used::

    - echo:
        msg: "Command returned: {{message[0]}}"

If the command returns a non-zero exit code, ScriptEngine issues an error and
stops.  However, if ``ignore_error`` is set to true and the command returns a
non-zero exit code, a warning is issued and ScriptEngine continues. Note that
YAML accepts, for example, the strings ``true``, ``True``, ``Yes``, ``ON`` as
true.


Context task
------------
Stores data in the ScriptEngine context.

Usage::

    base.context:
        <NAME>: <VALUE>

Example::

    base.context:
        planet: Earth
        some_countries:
            - Norway
            - Sweden
            - Finnland
            - Danmark
        number: 4


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
        msg: <MESSAGE> # optional


Find task
---------
Usage::

    base.find:
        path: <PATH>
        pattern: <SEARCH_PATTERN> # optional
        type: <FILE_OR_DIR> # optional


Getenv task
-----------
Reads an environment variable and stores it in the ScriptEngine context.

Usage::

    - base.getenv:
        name: <VAR_NAME>
        set: <NAME>

Example::

    - base.getenv:
        name: HOME
        set: home
    - base.echo:
        msg: "My {{home}} is my castle."


Include task
------------
Usage::

    - base.include:
        src: <PATH>
        ignore_not_found: <TRUE_OR_FALSE> # optional


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
        logging: <LOGLEVEL> # optional

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
        'debug': Logging to the debug logger§


Template task
-------------
Runs the template file given by ``src`` through the `Jinja2 Template Engine
<http://jinja.pocoo.org/>`_ and saves the result as a file at ``dst``.

Usage::

    base.template:
        src: <PATH>
        dst: <PATH>

ScriptEngine searches for the template file (``src``) in the following
directories, at the given order:

#. ``.``
#. ``./templates``
#. ``{{se.cli.cwd}}``
#. ``{{se.cli.cwd}}/templates``

where ``.`` is the current directory at the time when the ``template`` task
is executed and ``{{se.cli.cwd}}`` is the original working directory, the
working directory at the time when the ScriptEngine command line tool was
called.

It is important to note that ``src`` must contain a relative path, absolute
paths will not work.

The template file may refer to any of the configurations set by ``context``
tasks.


Time task
---------
Usage::

    base.time:
        set: <CONTEXT_VARIABLE>
        since: <DATETIME> # optional
