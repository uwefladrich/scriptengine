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

Tasks "do things". This can be simple things, like copying a file or writing a
message on the terminal. It could also be more complex things, like changeing a
date in a NetCDF file. Whatever the complexity of a task is, it will be hidden.
A task is listed in a script by it's name and some arguments, and later it is
run by a ScriptEngine instance to do it's actual work.

A number of different tasks are available when using ScriptEngine. In fact, one
of the main ideas with ScriptEngine is that it should be easy to develop and
provide new tasks for anything that users may need. Hence, a task should be
available for most of what users would want to do with ScriptEngine.

However, tasks are not "baked" into the ScriptEngine code. Instead, they are
loaded, at run time, from separate Python modules. Thus, tasks can easily be
provided by other packages and made available to the user when ScriptEngine is
run. Of course, there are packages for standard tasks that come with
ScriptEngine.

Technically, a task is a Python class that is derived from the ``Task`` class
that ScriptEngine provides. In fact, it is possible to use ScriptEngine from
within other Python programs, without ever defining tasks in YAML scripts.


Scripts
-------

Scripts, in the ScriptEngine terminology, are collections of tasks, described
in the YAML language. Usually, a script is a YAML file that represents a list
of tasks. How specific tasks are represented in YAML is usually intuitive, as
shown in the following example::

    - config:
        planet: Earth
    - echo:
        msg: "Hello, {{planet}}!"

This little script is the inevitable "Hello world" example in ScriptEngine! It
is run like this::

    se hello-world.yml

provided the little YAML snippet was stored in a file called
``hello-world.yml``.


ScriptEngine Instances
----------------------

Most of the time, the difference between the term ScriptEngine in general and
a ScriptEngine instance in particular is not very important.


Task Context
------------

An important concept in ScriptEngine is the task context, or short, the
context. The context is, technically, a dictionary, i.e. a data structure of
key, value pairs. ScriptEngine tasks can store and retrieve information from
the context.

When a ScriptEngine instance is created, the context is initialised. Some
information about the execution environment is stored by the ScriptEngine
instance in the new context. Then, it is passed to every task that is executed.
Usually, the context will be populated with information as tasks are processed.

We have already seen the usage of the context in the "Hello world" example
above. The ``config`` task stored a parameter named ``planet`` in the context
and the ``echo`` task used the information from the context to display it's
message.

Since the context is a Python dictionary, it can store any Python data types.
This is, for example, often used to structure information by storing further
dictionaries in the context. Numbers and dates are other examples for useful
data types for context information.


YAML
----


Jinja2 Templating
-----------------