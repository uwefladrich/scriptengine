Writing Scripts
===============

ScriptEngine scripts are written in YAML_. A basic understanding is therefore
needed about YAML syntax rules in order to write ScriptEngine scripts.

.. _YAML: https://foo.prg

Simple ScriptEngine scripts
---------------------------

Each ScriptEngine task is a YAML dictionary and a ScriptEngine script is
usually a list of tasks. Let's look at the simplest possible script::

    base.exit:
    
This script is not particularly helpful, it doesn't do anything at all.
Nevertheless, if you put this in a file, e.g. ``exit.yml``, and run:

.. code-block:: shell

    > se exit.yml

ScriptEngine will run the ``exit`` task and, well, exit. Technically, the script
contains the YAML dictionary ``{exit: null}``, which will be parsed by
ScriptEngine into the ``exit`` task.

Let's look at a slightly more useful example::

    base.echo:
        msg: Hello, world!

This is the inevitable Hello, world! example in ScriptEngine. Beside the name
of the task (``base.echo``, i.e. the ``echo`` task from the ``base`` package)
there is also an argument, ``msg``. From a YAML perspective, all task
arguments are the (key, value) pairs of a dictionary associated with the task
name.

Most scripts will contain more than one task and therefore will contain a YAML
list containing the tasks::

    - base.context:
        planet: Earth
    - base.echo:
        msg: "Hello, {{planet}}!"

This script will write "Hello, Earth!". There are two tasks: ``base.context``
and ``base.echo``, which are the two elements of a YAML list.


Do
--

The job specifier ``do`` allows for grouping a `list of tasks` inside one single
job (see :ref:`concepts:jobs`). For example::

    - do:
      - base.context:
          planet: Earth
      - base.echo:
          msg: "Hello, {{planet}}!"

This is most often used in order to apply a ``when`` clause or a ``loop`` to a
sequence of tasks.


Loops
-----

Jobs and tasks can be looped over. The simplest example is just a task with an
added ``loop`` specifier, such as::

  - base.echo:
      msg: "Looping over item, which is now {{item}}"
    loop: [1,2,3]

In this example, the ``base.echo`` task would be executed three times, with
``item`` taking the values of 1, 2, and 3. Here, the loop is specified by an
explicit list in YAML inline notation. A conventional block format notation
of the list works just the same::

  - base.echo:
      msg: "Looping over item, which is now {{item}}"
    loop:
      - 1
      - 2
      - 3

The list can also be specified in a separate ``base.context`` task, as in::

  - base.context:
      list: [1,2,3]
  - base.echo:
      msg: "Looping over item, which is now {{item}}"
    loop: "{{list}}"

Note that the string defining the loop list must be enclosed in quotes because
of the braces.

As the previous examples illustrate, the loop specifier must be a valid YAML list. There is,
however, some freedom in the way that list is constructed. For example, a common pattern is to
loop over a contiguous range of numbers. This can be accomplished by combining the Jinja
``range()`` function and ``list`` filter::

  - base.echo:
      msg: "Looping from one to five, now at {{item+1}}"
    loop: "{{range(5)|list}}"

In general, it is often useful to use the power of Jinja in order to contruct loops.

In all of the above examples, the loop index variable was not explicitly
named, which means it takes on its default name, ``item``. The ``item``
variable is added to the context for all jobs or tasks within the loop and can
be accessed using the usual syntax, as shown in the previous examples. After
the loop is completed, the variable is removed from the context, i.e. it is
*not* possible to access it from jobs or tasks that follow the loop.

It is possible to explicitly
define another name to the loop index variable, by using an extended loop
specifier. Here is an example::

  - base.echo:
      msg: "Looping over the 'foo' variable: {{foo}}"
    loop:
      with: foo
      in:   [1,2,3,4]

In that example, the loop index variable is named ``foo`` and it is added to
the context of all jobs and tasks defined in the loop, in the same manner as
the default ``item`` variable.

In case a loop variable (explicitly given or ``item``, by default) already
exists in the context when a loop is entered, ScriptEngine will issue a warning
about a colliding loop index variable. Nevertheless, the loop will still be
processed, with the loop variable value *hiding* the value of the variable with
the same name from outside the loop. After the loop has completed, the original
value of the variable is restored.

It is also possible to nest loops::

  - do:
      - base.echo:
          msg: "Nested loop: 'foo' is {{foo}} while 'bar' is {{bar}}"
        loop:
          with: foo
          in:   [1,2]
    loop:
      with: bar
      in:   [4,5,6]

In most cases, it will make sense to explicitly define the name of the loop
index variables in nested loops, although it *is* possible to rely on the
default variables. So the following example would work::

  - do:
      - base.echo:
          msg: "Nested loop: 'item' is {{item}}"
        loop: [1,2]
    loop: [4,5,6]

Nevertheless, ScriptEngine will, again, issue a warning about a loop index
variable collision. When using nested loops with the same loop index variable
(explicitly or by default), the variable values from outer loops will not be
accessible in the inner loops.

It is also possible to loop over dicts in ScriptEngine, like in the following
example::

    - base.echo:
        msg: "{{key}} is {{value}} years old."
      loop:
        in:
            Mary: 31
            Peter: 29
            Paul: 39

which would yield::

    Mary is 31 years old.
    Peter is 29 years old.
    Paul is 39 years old.

The example shows that the extended loop specifier with ``in:`` must be used
when looping over dicts, otherwise an *invalid loop descriptor error* error
occurs. Furthermore, the example shows that the default loop variables for loops
over dicts are ``key`` and ``value``. If the dict loop should use other
variables, their names can be given explicitly::

    - base.echo:
        msg: "{{name}} is {{age}} years old."
      loop:
        with: [name, age]
        in:
            Mary: 31
            Peter: 29
            Paul: 39

In the same manner as for lists, loop dicts can be defined in the ScriptEngine
context::

    - base.context:
        people:
            Mary: 31
            Peter: 29
            Paul: 39
    - base.echo:
        msg: '{{name}} is {{age}} years old.'
      loop:
        with: [name, age]
        in: '{{people}}'


Conditionals
------------

It is possible to control that a given job runs exclusively under a certain
condition, by using a ``when`` clause. Here is an example::

    - base.context:
        year: 1963
    - base.echo:
        msg: 'Peter, Paul and Mary most famous song'
      when: "{{year==1963}}"

.. hint::
    Because dict keys are not ordered in YAML, the second task in the previous
    example is equivalent to::

        - when: "{{year==1963}}"
          base.echo:
            msg: 'Peter, Paul and Mary most famous song'

    Some might find it easier to read if the condition precedes the task body.

The ``when`` clause can be combined with the ``do`` keyword, to execute a
sequence of tasks conditionally::

    - base.context:
        year: 1963
    - when: "{{year==1963}}"
      do:
        - base.echo:
            msg: 'Puff, the magic dragon'
        - base.echo:
            msg: 'lives by the sea'

.. note::
    There is no `else` clause in ScriptEngine. If the equivalent to an
    if-then-else logic is needed, two ``when`` clauses with complementary
    expressions must be used.


Special YAML Features
---------------------

YAML constructors
^^^^^^^^^^^^^^^^^
PyYAML_ (the YAML implementation used by ScriptEngine) allows user-defined
data types, which are indicated by a single exclamation mark (!).
ScriptEngine makes use of this feature to implement some advanced features:

Noparse strings
"""""""""""""""
Every time ScriptEngine reads a string argument value from a script, it
parses the value with Jinja2 (to make substitutions from the context and
other Jinja2 transformations) and, thereafter, once more with YAML (to
create correct data types, e.g. numbers, lists, dicts).

However, this leads sometimes to undesired results. Consider the following
``context`` task::

  base.context:
    first_name: Foo
    last_name: Bar
    full_name: "{{first_name}} {{last_name}}"

In the example, ``full_name`` gets assigned " " (a single space), because
``first_name`` and ``last_name`` are only effectively in the context *after*
the ``context`` task has completed.

ScriptEngine can be instructed to skip parsing the ``full_name`` argument in
this task, which would solve the problem in many cases, because when
``full_name`` is used later as (part of) any other argument, it is parsed
again, thus substituting ``first_name`` and ``last_name`` at a later stage.

To avoid parsing of an argument, use the ``!noparse`` YAML constructor::

  base.context:
    first_name: Foo
    last_name: Bar
    full_name: !noparse "{{first_name}} {{last_name}}"

which assigns the argument string ``{{first_name}} {{last_name}}`` literally
to ``full_name`` and delays parsing until later, when ``first_name`` and
``last_name`` are available from the context.

Another situation were parsing needs to be avoided is::

  base.echo:
    msg: "Foo: bar"

which would, unexpectedly, write "``{'Foo': 'bar'}`` instead of ``Foo: bar``
because YAML parsing would turn the string into a dictionary. Similar issues
would arise with other data types, like lists or dates/times. ``!noparse``
avoids the situation again::

  base.echo:
    msg: !noparse "Foo: bar"

and stores the string ``Foo: bar`` literally in the context.

While ``!noparse`` solves problems in most cases, a finer control over the
parsing is sometimes needed. It is possible to avoid either Jinja2 or YAML
parsing exclusively by using ``!noparse_jinja`` or ``!noparse_yaml``,
respectively.


RRULEs
""""""
ScriptEngine supports recurrence rules for dates and times, as defined in
RFC5545_ and implemented in the Python dateutil_ module. To create an RRULE
in a ScriptEngine script, use the ``!rrule`` constructor (for an explanation
of the ``>`` operator and multi-line strings, see below)::

  base.context:
    schedule: !rrule >
        DTSTART:19900101
        RRULE:FREQ=YEARLY;UNTIL=20000101

which would create a schedule with 11 yearly events, starting on January 1st
1990 and extending until, including, 2000. The specification is turned into a
``dateutil.rrule.rrule`` object, which is (in the above example) stored in the
context. It could be used elsewhere in the script to access, for example, the
year of the first event::

  base.echo:
    msg: "First event is in year {{schedule[0].year}}"


Multi-line strings
^^^^^^^^^^^^^^^^^^
Multi-line strings are defined in YAML and not a special feature of
ScriptEngine. They can be useful for writing scripts by allowing to split
long strings and make script more readable, or make it possible to format
output.
This is an example for using multi-line strings to format output::

  base.echo:
    msg: !noparse_yaml |
      This
      is a multi-line
      string
      with an answer: {{18+24}}.

YAML multi-line strings are either denoted by ``|``, in which case they are
preserving line breaks, or by ``>``, in which case they are not.

Note that in the example above, it is necessary to add ``!noparse_yaml``
because ScriptEngine would re-parse the multi-line string otherwise, removing
all line breaks. If there hadn't been a Jinja2 command in the string,
``!noparse`` would have been enough.


Jinja2 filters
--------------

ScriptEngine defines a number of additional `Jinja2 filters`_, which might be
useful for writing scripts.

Filters to handle dates and times
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

datetime
    Converts a string to a ``datetime.datetime`` object, for example::

        base.context:
            date_time: "{{ '2022-01-01 00:00:00' | datetime }}""

    The format of the string defaults to ``%Y-%m-%d %H:%M:%S``, but it can be
    changed::

        base.context:
            date_time: "{{ '2022/01/01 00:00:00' | datetime('%Y/%m/%d %H:%M:%S') }}""

increment_datetime
    Increment a ``datetime.datetime`` object by a number of days, hours, minutes
    or seconds, for example::

        base.context:
            date_time: "{{ '2022-01-01 00:00:00' | datetime | increment_datetime(days=1, hours=6)}}""

date
    Converts a string to a ``datetime.date`` object::

        base.context:
            start_date: "{{ '2022-01-01 00:00:00' | date }}""

    The format of the date string can be changed the same way as for the
    **datetime** filter.

Filters to handle paths and filenames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

basename
    Returns the base name of a part (i.e. the path with all but the last part
    removed)::

        - base.context:
            file: /path/to/file.txt
        - base.copy:
            src: "{{ file }}"
            dst: "/new/path/to/{{ file | basename }}"


dirname
    Returns the directory part of a path (i.e. the part with the base name
    removed)::

        - base.context:
            file: /path/to/file.txt
        - base.copy:
            src: "{{ file }}"
            dst: "{{ file | dirname }}/new_file.txt"


exists
    Returns true if the path exists, otherwise false::

        when: "{{ '/path/to/file' | exists }}"
        echo:
            msg: Yes, file exists!


path_join
    Composes path from components::

        base.echo:
            msg: "{{ ['foo', 'bar.txt'] | path_join }}"

Other filters
^^^^^^^^^^^^^

render
    Renders the expression (e.g. a variable) with Jinja2 and the current context. This can be used, for
    example, to explicitly render context parameters that have been set with the `!noparse` tag::

        - base.context:
            foo: me
            bar: !noparse "{{ foo }}"
        - when "{{ bar|render == 'me' }}"
          base.echo:
            msg: "It is {{ bar }}!"

    Without using the `render` filter in the example, the `when` clause would evaluate to `false` because
    the value of `bar` would still be `"{{ foo }}"` because of `!noparse`.


.. _PyYAML: https://pyyaml.org
.. _RFC5545: https://tools.ietf.org/html/rfc5545
.. _dateutil: https://dateutil.readthedocs.io/en/stable/rrule.html
.. _`Jinja2 filters`: https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-filters
