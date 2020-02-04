Introduction
============

The main purpose of ScriptEngine is to replace shell scripts. ScriptEngine
tries to put the user's focus on the description of common shell script tasks,
rather than their implementation. Ideally, the description of a complex task
should be nearly as short and clear as the description of a simpler one.

The ScriptEngine concept separates scripts (*what* to do) from the
implementation of tasks (*how* to do things), and the actual execution
environment (the script engine instances). This allows different execution
models to be implemented. A simple script engine instance may execute tasks
from a script as a simple sequential list, which is, in fact, the default
behaviour in ScriptEngine. However, it is rather easy, within the ScriptEngine
concept, to implement more advanced script engine instances, such as one that
executes tasks in parallel or sends tasks to batch systems.

A major theme in the ScriptEngine implementation is to combine modern
programming techniques, such as Python, YAML syntax, and Jinja2 templating, in
clever ways such that as little as possible is left for actual implementation.

ScriptEngine is heavily inspired by Ansible. However, there are some important differences:

- ScriptEngine is made to run tasks locally. Or, to put it the other way
  around, ScriptEngine is usually run on the same machine where tasks need to
  be executed.

- ScriptEngine scripts usually describe what is to be done, not a desired state
  of things.

- ScriptEngine is *not* focused on system administration. Although this is not
  part of the underlying concept, it will most probably reflect in the
  selection of available tasks.

- ScriptEngine's implementation of tasks is extremely lightweight, they're
  basically single Python functions. Almost every user should be able to add
  new tasks to ScriptEngine.
