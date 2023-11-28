Installation
============

Prerequisites
-------------

ScriptEngine needs Python version 3.8 or newer. To check the version of your
default Python installation, run:

.. code-block:: shell

    > python --version

If the version is 3.8 or larger, everything is fine. If the default Python
version is 2, check if Python3 is still available:

.. code-block:: shell

    > python3 --version

If that returns a version >=3.8, you need to specify the Python3 interpreter
explicitly in the installation below.


Install in a Python Virtual Environment
---------------------------------------

ScriptEngine is preferably installed in a Python virtual environment. There are
different ways to create virtual environments, for example with virtualenv_ or
venv_. The ``venv`` module is part of the Python standard library and has been
recommended for creating virtual environments since Python 3.5, Hence, it is
used here to explain the ScriptEngine installation.

Load the ``venv`` module from the ``python`` executable (if your default Python
is version 3, otherwise use ``python3``) to create a virtual environment for
ScriptEngine:

.. code-block:: shell

    > python -m venv .se

The ``.se`` argument is just an arbitrary name for the virtual environment and
the corresponding directory. You can chose any name, but it can be convenient
to chose a hidden directory.

Activate the created virtual environment:

.. code-block:: shell

    > source .se/bin/activate

The ``venv`` module will also install the ``pip`` package manager in the
virtual environment. Once the virtual environment is activated, use ``pip`` to
install ScriptEngine, along with its dependencies, from the Python Package
Index (PyPI_):

.. code-block:: shell

    (.se)> pip install scriptengine

Test the ScriptEngine installation with:

.. code-block:: shell

    (.se)> se --version

which should display the ScriptEngine version.


Install under Anaconda
----------------------

It is sometimes preferable to install ScriptEngine within Anaconda_, a Python
distribution that provides a rich set of packages for scientific computing. In
particular, this is needed if additional ScriptEngine task packages have
dependencies that can only be satisfied with the conda_ package manager.

Assuming that the ``conda`` command is available, create and activate a virtual
environment (named ``se`` in the following example) for ScriptEngine:

.. code-block:: shell

    > conda create -n se
    > activate se

ScriptEngine is available as package from the ``conda-forge`` channel, so
installation is as easy as

.. code-block:: shell

    (se)> conda install -c conda-forge scriptengine

Test if ScriptEngine works in your ``conda`` environment:

.. code-block:: shell

    (se)> se --version


Development installation
------------------------

ScriptEngine can be installed directly from a local directory. This can be
useful for testing own developments or changes that have not yet been
published as a package on PyPi. For example, ScriptEngine can be installed
from a clone of the Github repository:

.. code-block:: shell

    (.se)> git clone https://github.com/uwefladrich/scriptengine.git
    (.se)> cd scriptengine
    (.se)> pip install -e .

This will install ScriptEngine along with its dependencies very similar to
installing from PyPI. However, any changes made in the local directory will
immediately affect the ScriptEngine installation.


.. _PyPI: https://pypi.org
.. _Anaconda: https://anaconda.com
.. _conda: https://conda.io
.. _venv: https://docs.python.org/3/library/venv.html
.. _virtualenv: https://virtualenv.pypa.io/en/latest
