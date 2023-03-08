Command Line Interface
======================

The ScriptEngine command line interface is provided by the ``se`` script. The
command provides basic help when running it with the ``-h`` or ``--help``
flag:

.. code-block:: shell

    > se --help
    usage: se [-h] [-V] [--loglevel {debug,info,warning,error,critical}]
              [--nocolor]
              files [files ...]

    ScriptEngine command line tool

    positional arguments:
      files                 YAML file(s) to read

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show ScriptEngine version and exit
      --loglevel {debug,info,warning,error,critical}
                            The minimum level of log messages that is displayed.
                            For verbose output, use "debug". For minimal output,
                            use "error" or "critical".
      --nocolor             do not use colored terminal output

    Available ScriptEngine tasks: hpc.slurm.sbatch, base.chdir, base.command,
    base.context, base.copy, base.echo, base.exit, base.find, base.getenv,
    base.include, base.link, base.make_dir, base.move, base.remove,
    base.task_timer, base.template, base.time

Using the ``-V`` or ``--version`` option displays the current ScriptEngine version:

.. code-block:: shell

    > se --version
    0.8.5

One or more scripts can be passed to ScriptEngine as arguments:

.. code-block:: shell

    > se hello.yml
    2021-03-18 09:54:40 INFO [se.cli] Logging configured and started
    2021-03-18 09:54:40 INFO [se.task:echo <37f189f217>] Hello, world!
    Hello, world!

As seen above, ScriptEngine and ScriptEngine tasks provide information during
the run via logging, usually as output to the terminal. The amount of
information can be controlled by setting the ``--loglevel``:

.. code-block:: shell

    > se --loglevel debug hello.yml
    2021-03-18 09:58:04 INFO [se.cli] Logging configured and started
    2021-03-18 09:58:04 DEBUG [se.cli] Loaded task base.chdir: Chdir from scriptengine.tasks.base.chdir
    2021-03-18 09:58:04 DEBUG [se.cli] Loaded task base.command: Command from scriptengine.tasks.base.command
    [...]
    2021-03-18 09:58:04 DEBUG [se.cli] Loaded task base.time: Time from scriptengine.tasks.base.time
    2021-03-18 09:58:04 DEBUG [se.task:echo <aa66c50601>] Created task: Echo: Hello, world!
    2021-03-18 09:58:04 INFO [se.task:echo <aa66c50601>] Hello, world!
    Hello, world!

    > se --loglevel error hello.yml 
    Hello, world!

Usually, the logging output is colored (not seen in this documentation). This
is done on the terminal with ANSI escape codes, but it may be undesired, for
example, when the output is stored in a logfile. Hence, colored output can be
switched of with the ``--nocolor`` argument.

As seen in the output of ``se --help`` above, ScriptEngine lists all
available task in the current installation. ScriptEngine uses dynamic task
loading (see :ref:`Concepts`) and additional task can be installed from
Python packages. In the example above, all tasks from the build-in ``base.*``
package are available. Furthermore, the ``hpc.slurm.sbatch`` task is
provided, which comes from the ``scriptengine-tasks-hpc`` (go `there`_) Python
package.

Note that ScriptEngine task names follow a namespace scheme to prevent name
clashes for tasks from different packages.

.. _there: https://pypi.org/project/scriptengine-tasks-hpc/
