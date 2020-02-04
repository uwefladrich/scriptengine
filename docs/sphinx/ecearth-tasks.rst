EC-Earth tasks
==============

ScriptEngine tasks that are specific to the EC-Earth model.


UpdateEceinfo task
------------------

This task reads an ``ece.info`` file and updates the ScriptEngine context by
storing updated values under the ``eceinfo`` key.

Usage::

    - update_eceinfo:
        path: <PATH>

Example::

    - update_eceinfo:
        path: "{{rundir}}/ece.info"
    - echo:
        msg: "The current leg is {{eceinfo.leg}}"



WriteEceinfo task
-----------------

This task appends the information currently stored in the ScriptEngine context
under the ``eceinfo`` key to an ``ece.info`` file.

Usage::

    - write_eceinfo:
        path: <PATH>

If the ``eceinfo`` key is not found in the ScriptEngine context (for example,
because no UpdateEceinfo task was previously executed), a warning is issued.
