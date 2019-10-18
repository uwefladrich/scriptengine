Basic tasks
===========


Config task
-----------

Usage::

    - config:
        <NAME>: <VALUE>


Echo task
---------

Displays a customised message.

Usage::

    - echo:
        msg: <MESSAGE>

Example::

    - config:
        planet: Earth
    - echo:
        msg: "Hello, {{planet}}!"


Include task
------------

Usage::

    - include:
        src: <PATH>
