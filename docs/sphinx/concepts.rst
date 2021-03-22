Concepts
========

Working with ScriptEngine does not require knowledge about it's underlying
implementation architecture in detail, but it is useful to understand a few
basic concepts and terms. It is, for example, good to know how `tasks` and
`scripts` are understood in the ScriptEngine world. Furthermore, a few
technical topics are important when using ScriptEngine, in particular some
details about the YAML format and how templating with Jinja2 works.


Tasks
-----

A task is the basic unit of work for ScriptEngine. It is the building block for
scripts (see next section) and also the individual item a ScriptEngine instance
(see even later) will handle.

Tasks "do things". This can be simple things, like copying a file or writing
a message on the terminal. It could also be more complex things, involving
more complex computations, file operations, or interactions with services.
But whatever the actual complexity of a task is, it will be hidden. A task is
listed in a script by it's name and some arguments, and later it is run by a
ScriptEngine instance to do it's actual work.

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
is run like this::

    > se hello-world.yml

provided the little YAML snippet was stored in a file called
``hello-world.yml``. Please not that ScriptEngine uses a dot notation for the
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

When a ScriptEngine instance is created, the context is initialised. Some
information about the execution environment is stored by the ScriptEngine
instance in the new context. Then, it is passed to every task that is executed.
Usually, the context will be populated with information as tasks are processed.

We have already seen the usage of the context in the "Hello world" example
above. The ``context`` task stored a parameter named ``planet`` in the context
and the ``echo`` task used the information from the context to display it's
message.

Since the context is a Python dictionary, it can store any Python data types.
This is, for example, often used to structure information by storing further
dictionaries in the context. Numbers and dates are other examples for useful
data types for context information.


YAML
----

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
