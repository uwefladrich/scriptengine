# ScriptEngine

The main purpose of ScriptEngine is to replace shell scripts. ScriptEngine
tries to put the user’s focus on the description of common shell script tasks,
rather than their implementation. Ideally, the description of a complex task
should be nearly as short and clear as the description of a simpler one.

The ScriptEngine concept separates scripts (what to do) from the implementation
of tasks (how to do things), and the actual execution environment (the script
engine instances). This allows different execution models to be implemented. A
simple script engine instance may execute tasks from a script as a simple
sequential list, which is, in fact, the default behaviour in ScriptEngine.
However, it is rather easy, within the ScriptEngine concept, to implement more
advanced script engine instances, such as one that executes tasks in parallel
or sends tasks to batch systems.

Since ScriptEngine tasks are basically Python class methods, there is a wide
range of tools available to get the actual work done, which allows for a more
efficient implementation of tasks.
