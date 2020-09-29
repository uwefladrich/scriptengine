Basic tasks
===========


Context task
------------

Stores data in the ScriptEngine context.

Usage::

    - context:
        <NAME>: <VALUE>

Example::

    - context:
        planet: Earth
        some_countries:
            - Norway
            - Sweden
            - Finnland
            - Danmark
        number: 4


Echo task
---------

Displays a customised message.

Usage::

    - echo:
        msg: <MESSAGE>

Example::

    - context:
        planet: Earth
    - echo:
        msg: "Hello, {{planet}}!"


Include task
------------

Usage::

    - include:
        src: <PATH>
