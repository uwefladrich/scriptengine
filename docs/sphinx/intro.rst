Introduction
============

ScriptEngine is a lightweight and extensible framework and tool for executing
scripts written in YAML. The main purpose of ScriptEngine is to replace shell
scripts in situations where highly configurable and modular scripts are needed.
ScriptEngine relies on YAML_ and makes extensive use of Jinja2_ templating to
provide a comprehensive scripting language. This allows users to put focus on
the description of tasks, rather than their implementation. The description of
complex tasks should be nearly as short and clear as for simpler ones.

The ScriptEngine concept separates scripts (*what* to do) from the
implementation of tasks (*how* to do things), and also from the actual
execution environment (the script engine instances). This modularity allows the
provision of different execution models (e.g. sequential or parallel; local or
remote) within the same framework.

ScriptEngine provides a concise set of basic tasks that users can use to write
their scripts. However, extensibility is a fundamental principle for
ScriptEngine. Complementary task sets are provided as Python packages that can
be loaded into ScriptEngine at run time. Thus, the capabilities of ScriptEngine
scripts extend to features provided by task set packages available from package
repositories or locally.

ScriptEngine tasks are simple Python classes with a ``run()`` method, which
means that it is rather easy to build new tasks sets for particular needs. And
because everything is based on Python3, there is a wide range of modules
available to get the actual work done easily and efficiently.

ScriptEngine is strongly influenced by Ansible_. In fact, ScriptEngine was
developed because it met almost, but not quite, the needs of the author. Here
are some important differences:

- Tasks are executed on a single host, often the host where the ScriptEngine
  command line tool is running. This is not an implication of any ScriptEngine
  concept, though. It would be possible to implement ScriptEngine instances
  that execute tasks remotely, or on multiple hosts.

- Contrary to Ansible, ScriptEngine tasks specify actions, not states.

- ScriptEngine is *not* focused on system administration. Although this is not
  part of the underlying concept, it will most probably reflect in the
  selection of available tasks.

- ScriptEngine's implementation of tasks is extremely lightweight, they're
  basically single Python functions. Almost every user should be able to add
  new tasks to ScriptEngine.


ScriptEngine is easily installed from the *Python Package Index* (PyPI_) with
the pip_ package manager.

.. _YAML: https://yaml.org
.. _Jinja2: https://jinja.palletsprojects.com
.. _Ansible: https://ansible.com
.. _PyPI: https://pypi.org
.. _pip: https://pip.pypa.io