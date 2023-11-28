Concepts
========

Working with ScriptEngine does not require knowledge about its underlying
implementation architecture in detail, but it is useful to understand a few
basic concepts and terms. It is, for example, good to know how `tasks` and
`scripts` are understood in the ScriptEngine world. Furthermore, a few
technical topics are important when using ScriptEngine, in particular some
details about the YAML format and how templating with Jinja2 works.


Tasks
-----

A task is the basic unit of work for ScriptEngine. It is the building block for
scripts (see `Scripts` section) and also the individual item a ScriptEngine instance
(see even later) will handle.

Tasks "do things". This can be simple things, like copying a file or writing
a message on the terminal. It could also be more complex things, involving
more complex computations, file operations, or interactions with services.
But whatever the actual complexity of a task is, it will be hidden. A task is
listed in a script by its name and some arguments, and later it is run by a
ScriptEngine instance to do its actual work.

A number of different tasks are available when using ScriptEngine. In fact, one
of the main ideas with ScriptEngine is that it should be easy to develop and
provide new tasks for anything that users may need. Hence, a task should be
available for most of what users would want to do with ScriptEngine.

However, tasks are not "baked" into the ScriptEngine code. Instead, they are
loaded, at run time, from separate Python modules. Thus, tasks can easily be
provided by other packages and made available to the user when ScriptEngine is
run. ScriptEngine comes with a basic package of tasks that are often used,
but it can be adapted to a wide range of fields by providing specialised task
packages.

Technically, a task is a Python class that is derived from the ``Task`` class
that ScriptEngine provides. In fact, it is possible to use ScriptEngine from
within other Python programs, without ever defining tasks in YAML scripts.


Jobs
----

Similar to tasks, `jobs` are units of work for ScriptEngine. Jobs can extend
tasks in two ways:

    * jobs can join a number of tasks into a sequence, and
    * jobs can add conditionals and loops to tasks.

Corresponding to these two cases, jobs use the special ``do`` keyword to specify
sequences of tasks (see :ref:`do <scripts:do>`), and/or ``when`` or ``loop``
clauses clauses to specify :ref:`conditionals <scripts:conditionals>` and
:ref:`loops <scripts:loops>`, respectively.


Scripts
-------

Scripts, in the ScriptEngine terminology, are collections of tasks, described
in the YAML language. Usually, a script is a YAML file that represents a list
of tasks. How specific tasks are represented in YAML is usually intuitive, as
shown in the following example::

    - base.context:
        planet: Earth
    - base.echo:
        msg: "Hello, {{planet}}!"

This little script is the inevitable "Hello world" example in ScriptEngine! It
is run like this:

.. code-block:: shell

    > se hello-world.yml

provided the little YAML snippet was stored in a file called
``hello-world.yml``. Please note that ScriptEngine uses a dot notation for the
naming of tasks. This allows tasks from different task packages to coexist
without conflict. The tasks in the above example come from the ``base`` task
package, which is an integral part of ScriptEngine. Nevertheless, beside
being always available, there is no technical difference between the ``base``
task package and others.


ScriptEngine Instances
----------------------

Most of the time, the difference between the term ScriptEngine in general and a
ScriptEngine instance in particular is not very important. However, technically,
scripts are given to a particular ScriptEngine instance for execution. Different
types of ScriptEngine instances could exist, allowing for different execution
models to be implemented. For example, a ScriptEngine instance could allow tasks
to be run in parallel, or to be submitted to remote hosts for execution.

For now, ScriptEngine provides ``SimpleScriptEngine``, which takes scripts and
executes tasks sequentially, on the local host.


Task Context
------------

An important concept in ScriptEngine is the task context, or short, the
*context*. The context is, technically, a dictionary, i.e. a data structure of
key, value pairs. ScriptEngine tasks can store and retrieve information from the
context.

When a ScriptEngine :ref:`instance <concepts:scriptengine instances>` is
created, the context is initialised. Some information about the execution
environment is stored by the ScriptEngine instance in the new context. Then, it
is passed to every task that is executed.  Usually, the context will be
populated with information as tasks are processed.

We have already seen the usage of the context in the "Hello world" example
above. The ``base.context`` task stored a parameter named ``planet`` in the
context and the ``base.echo`` task used the information from the context to
display its message.

Since the context is a Python dictionary, it can store any Python data types.
This is, for example, often used to structure information by storing further
dictionaries in the context. Numbers and dates are other examples for useful
data types for context information.

The ScriptEngine task context extends the functionality of a Python dictionary
in two important aspects:

- allow for "dotted keys" in order to access nested dictionary values,
- allow for merging of contexts with the help of `deepmerge
  <https://deepmerge.readthedocs.io/en/latest/>`_,
- allow to store and load the context from/to a file.

Dotted keys are helpful for writing ScriptEngine scripts in YAML, because they
can substantially shorten the syntax when working with the context. See the
description of the :ref:`base-tasks:``base.context``` task for examples. Using
dotted keys can also simplify the access to context parameters in Jinja
experssions.

Context merging is a central concept for ScriptEngine. When tasks are executed,
they are allowed to update the context. These updates are implemented as deep
merges of the context dictionary, which makes it possible to add keys to nested
levels of the dictionary, or add items to lists.

Last not least, storing the context in, and loading from, a file, allows
ScriptEngine to achieve persistency. This enables, among other possibilities, to
pick off the context from a previous run.

.. versionadded:: 1.0
    Dotted keys and context load/store.


YAML
----

Short examples of important YAML structures follow below. For further
explanation and links, refer to the `YAML homepage <https://yaml.org/>`_.

YAML syntax for lists::

    - apple
    - pear
    - peach
    - banana

Compact list syntax::

    [apple, pear, peach, banana]

A YAML dictionary::

    name: apple
    color: green
    price: 0.2

Compact syntax::

    {name: apple, color: green, price: 0.2}

A list of dictionaries::

    - name: apple
      color: green
      price: 0.2
    - name: pear
      color: pink
      price: 0.4
    - name: banana
      color: yellow
      price: 0.7

A dictionary with lists::

    name: apple
    color: green
    price: 0.2
    vitamins:
        - C
        - B6
        - B2
        - K

YAML treats all terms as objects of no particular type. However, the Python YAML
parser will convert terms into Python objects of the appropriate type, for
example::

    number: 2
    another_number: 3.21
    string: This is a string
    another_string: "This is a quoted string"
    a_date: 2020-08-13


Jinja2 Templating
-----------------

`Jinja homepage and documentation <https://jinja.palletsprojects.com>`_
