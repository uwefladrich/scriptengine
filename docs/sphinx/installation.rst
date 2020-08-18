Installation
============

Prerequisites
-------------

ScriptEngine needs Python version 3.6 or newer. To check the version of your
default Python installation, run::

    > python --version

If the version is 3.6 or larger, everything is fine. If the default Python version is 2, check if Python3 is still avalable::

    > python3 --version

If that returns a verison >=3.6, you need to specify the Python3 interpreter
explicitely in the installation below.


Install in a Python Virtual Environment
---------------------------------------

The ``virtualenv`` package is needed, usually available with the system's
package manager. Create a Python virtual environment (if your default Python
version is 3.6 or above)::

    > virtualenv .se

Note that ``.se`` is just an arbitrary name for the virtual environment and the
corresponding directory. You can chose any name, but it is often convenient to
chose a hidden directory.

If the default Python version is 2, but Python3 is available, use::

    > virtualenv -p python3 .se

Activate the created virtual environment::

    > source .se/bin/activate

The ``virtualenv`` command will also install the ``pip`` package manager in the
virtual environment. Use ``pip`` to install ScriptEngine, along with it's
dependencies, from the Python Package Index (PyPI_)::

    (.se)> pip install scriptengine

Test the ScriptEngine installation with::

    (.se)> se --version

which should display the ScriptEngine version.


Install under Anaconda
----------------------

It is sometimes preferable to install ScriptEngine within Anaconda_, a Python
distribution that provides a rich set of packages for scientific computing. In
particular, this is needed if additional ScriptEngine task packages have
dependencies that can only be satisfied with the conda_ package manager.

Assuming that the ``conda`` command is available, create and activate a virtual
environment (named ``se`` in the following example) for ScriptEngine::

    > conda create -n se
    > activate se

Install ``pip`` in the virtual environment. This is needed, since ScriptEngine
is still installed from PyPI::

    (se)> conda install pip

Finally, install ScriptEngine in the ``conda`` environmen::

    (se)> pip install scriptengine

Test if ScriptEngine works in your ``conda`` environment::

    (se)> se --version


.. _PyPI: https://pypi.org
.. _Anaconda: https://anaconda.com
.. _conda: https://conda.io