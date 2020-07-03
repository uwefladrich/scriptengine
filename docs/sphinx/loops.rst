Loops
=====

Jobs and tasks can be looped over. The simplest example is just a task with an
added ``loop`` specifier, such as::

  - echo:
      msg: "Looping over item, which is now {{item}}"
    loop: [1,2,3]

In this example, the ``echo`` task would be executed three times, with ``item``
taking the values of 1, 2, and 3. Here, the loop is specified by an explicit
list in YAML inline notation. A conventional block format notation of the list
works just the same::

  - echo:
      msg: "Looping over item, which is now {{item}}"
    loop:
      - 1
      - 2
      - 3

The list can also be specified in a separate ``context`` task, as in::

  - context:
      list: [1,2,3]
  - echo:
      msg: "Looping over item, which is now {{item}}"
    loop: "{{list}}"

Note that the string defining the loop list must be enclosed in quotes because
of the braces.

In all of the above examples, the loop index variable was not explicitely
named, which means it takes on it's default name, ``item``. The ``item``
variable is added to the context for all jobs or tasks within the loop and can
be accessed using the usual syntax, as shown in the previous examples. After
the loop is completed, the variable is removed from the context, i.e. it is
*not* possible to access it from jobs or tasks that follow the loop.

It is possible to explicitely
define another name to the loop index variable, by using an extended loop
specifier. Here is an example::

  - echo:
      msg: "Looping over the 'foo' variable: {{foo}}"
    loop:
      with: foo
      in:   [1,2,3,4]

In that example, the loop index variable is named ``foo`` and it is added to
the context of all jobs and tasks defined in the loop, in the same manner as
the default ``item`` variable.

In case a loop variable (explicitely given or ``item``, by default) already
exists in the context when a loop is entered, ScriptEngine will issue a warning
about a colliding loop index variable. Nevertheless, the loop will still be
processed, with the loop variable value *hiding* the value of the variable with
the same name from outside the loop. After the loop has completed, the original
value of the variable is restored.

It is also possible to nest loops::

  - do:
      - echo:
          msg: "Nested loop: 'foo' is {{foo}} while 'bar' is {{bar}}"
        loop:
          with: foo
          in:   [1,2]
    loop:
      with: bar
      in:   [4,5,6]

In most cases, it will make sense to explicitely define the name of the loop
index variables in nested loops, although it *is* possible to rely on the
default variables. So the following example would work::

  - do:
      - echo:
          msg: "Nested loop: 'item' is {{item}}"
        loop: [1,2]
    loop: [4,5,6]

Nevertheless, ScriptEngine will, again, issue a warning about a loop index
variable collision. When using nested loops with the same loop index variable
(explicitely or by default), the variable values from outer loops will not be
accessible in the inner loops.
