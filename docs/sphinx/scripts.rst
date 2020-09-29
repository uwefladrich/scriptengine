Writing Scripts
===============

ScriptEngine scripts are written in YAML_. A basic understanding is therefore
needed about YAML syntax rules in order to write ScriptEngine scripts.

.. _YAML: https://foo.prg

Simple ScriptEngine scripts
---------------------------

Each ScriptEngine task is a YAML dictionary and a ScriptEngine script is usually
a list of tasks. Let's look at the simplest possible script::

    exit:
    
This script is not particularly helpful, it doesn't do anything at all.
Nevertheless, if you put this in a file, e.g. ``exit.yml``, and run::

    > se exit.yml

ScriptEngine will run the ``exit`` task and, well, exit. Technically, the script
contains the YAML dictionary ``{exit: null}``, which will be parsed by
ScriptEngine into the ``exit`` task.

Let't look at a slightly more useful example::

    echo:
        msg: Hello, world!

This is the inevitable Hello, world! example in ScriptEngine. Beside the name of
the task (``echo``) there is also an argument, ``msg``. From a YAML perspective,
all task arguments are the (key, value) pairs of a dictionary associated with
the task name.

Most scripts will contain more than one task and therefore will contain a YAML
list containing the tasks::

    - context:
        planet: Earth
    - echo:
        msg: "Hello, {{planet}}!"

This script will write "Hello, Earth!". There are two tasks: ``context`` and
``echo``, which are the two elements of a YAML list.


Loops
-----



Conditionals (`when` clauses)
-----------------------------



Special YAML Features
---------------------

### Multi-line strings


### RRULEs



### noeval strings
