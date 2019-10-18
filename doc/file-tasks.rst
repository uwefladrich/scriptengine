File tasks
==========

File tasks can be used to create, modify or delete objects (files, directories,
symbolic links) on the file system.


Copy task
---------

This task copies the file or directory given by ``src`` to ``dst``. If ``src``
is a file and ``dst`` is a directory, the ``src`` file is copied into the
``dst/`` directory. If ``src`` is a directory, ``dst`` must be a directory as
well and ``src`` is copied recursively into ``dst/``. When a directory is
copied, symbolic links are preserved.

Usage::

    - copy:
        src: <PATH>
        dst: <PATH>

When copying a file and the ``dst`` exists already, it is overwritten and a
waring is issued. When copying a directory and the ``dst`` exists already, an
``RuntimeError`` is raised.


Move task
---------

Usage::

    - move:
        src: <PATH>
        dst: <PATH>


Link task
---------

Creates a symbolic link with name given by ``dst``, which is pointing to the
path given by ``src``.

Usage::

    - link:
        src: <PATH>
        dst: <PATH>

When the ``dst`` path (i.e. the link target) does not exist, the link is still
created and a warning is issued.


Remove task
-----------

Removes a file, link, or directory. Directories are recursively deleted,
effectively removing all files and subdirectories that it contains.

Usage::

    - remove:
        path: <PATH>

When ``path`` does not exist, an info message is displayed (no warning or
error).



MakeDir task
------------

Creates a new directory at the given ``path``.


Usage::

    - make_dir:
        path: <PATH>

If ``path`` already exists, an info message is displayed (no warning or error).
When ``path`` is a file or symbolic link, a ``RuntimeError`` is raised.


Template task
-------------

Usage::

    - template:
        src: <PATH>
        dst: <PATH>
