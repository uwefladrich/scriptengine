System tasks
============



Getenv task
-----------

Reads an environment variable and stores it in the ScriptEngine context.

Usage::

    - getenv:
        name: <VAR_NAME>
        context: <NAME>

Example::

    - getenv:
        name: HOME
        context: home
    - echo:
        msg: "My {{home}} is my castle."



Command task
------------

Executes a command, with optional arguments.

Usage::

    - command:
        name: <COMMAND_NAME>
        args: <LIST_OF_ARGS> # optional
        cwd: <PATH> # optional
        stdout: <STRING> # optional
        ignore_error: [true|false] # optional

When ``cwd`` (current work directory) is specified, the command is executed in
the given directory::

    - command:
        name: ls
        args: [-l]
        cwd: /tmp

When the ``stdout`` is given, the standard output of the command is captured
and stored in the ScriptEngine context, for example::

    - command:
        name: echo
        args: [ Hello, World! ]
        stdout: message
    - echo:
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


Exit task
---------

Requests ScriptEngine to stop, optionally displaying a customised message.

Usage::

    - exit:
        msg: <MESSAGE> # optional
