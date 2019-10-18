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

Executes a command, optionally with arguments and possibly after changing the directory.

Usage::

    - command:
        name: <COMMAND_NAME>
        args: <LIST_OF_ARGS> # optional
        cwd: <PATH> # optional

Example::

    - command:
        name: ls
        args: [-l]
        cwd: /tmp



Exit task
---------

Requests ScriptEngine to stop, optionally displaying a customised message.

Usage::

    - exit:
        msg: <MESSAGE> # optional
