# ScriptEngine

ScriptEngine is a lightweight and extensible framework for executing scripts
written in YAML. The main purpose of ScriptEngine is to replace shell scripts
in situations where highly configurable and modular scripts are needed.
ScriptEngine relies on [YAML](https://yaml.org/) and makes extensive use of
[Jinja2](https://palletsprojects.com/p/jinja/) templating to provide a
comprehensive scripting language. This allows users to put focus on the
description of tasks, rather than their implementation. The description of
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
scripts is only limited by available task sets.

ScriptEngine tasks are simple Python classes with a `run()` method, which means
that it is rather easy to build new tasks sets for particular needs. And
because everything is based on Python3, there is a wide range of modules
available to get the actual work done easily and efficiently.

ScriptEngine is [open source](LICENSE) software, hosted at
[GitHub](https://github.com/uwefladrich/scriptengine). ScriptEngine packages
are provided at [PyPI](https://pypi.org/project/scriptengine/), so installation
is as easy as `pip install scriptengine`. Documentation, including more
detailed installation instructions, is published at
[ReadtheDocs](https://scriptengine.readthedocs.io/en/latest/).
