import setuptools

if __name__ == "__main__":
    tests = ["coverage", "coveralls", "pytest"]
    docs = ["sphinx", "sphinx-rtd-theme"]
    setuptools.setup(
        # The information below is duplicated from pyproject.toml.
        # This is because, for Python 3.6, we are stuck with older versions of
        # setuptools.setup(), which do not read this info directly from
        # pyproject.toml. Hence, we have to keep this redundancy until
        # ScriptEngine drops support for Python 3.6
        name="scriptengine",
        version="0.14.4",
        install_requires=[
            "importlib_metadata; python_version<'3.8'",
            "python-dateutil",
            "deepmerge",
            "deepdiff>=5.7.0,!=6.2.0,!=6.2.1",
            "PyYAML",
            "jinja2",
        ],
        extras_require={"tests": tests, "docs": docs, "all": tests + docs},
        entry_points={
            "console_scripts": [
                "se = scriptengine.cli.se:main",
            ],
            "scriptengine.tasks": [
                # Legacy task names, deprecated
                "chdir = scriptengine.tasks.base.chdir:Chdir",
                "command = scriptengine.tasks.base.command:Command",
                "context = scriptengine.tasks.base.context:Context",
                "copy = scriptengine.tasks.base.file.copy:Copy",
                "echo = scriptengine.tasks.base.echo:Echo",
                "exit = scriptengine.tasks.base.exit:Exit",
                "find = scriptengine.tasks.base.find:Find",
                "include = scriptengine.tasks.base.include:Include",
                "link = scriptengine.tasks.base.file.link:Link",
                "make_dir = scriptengine.tasks.base.file.make_dir:MakeDir",
                "move = scriptengine.tasks.base.file.move:Move",
                "remove = scriptengine.tasks.base.file.remove:Remove",
                "task_timer = scriptengine.tasks.base.task_timer:TaskTimer",
                "template = scriptengine.tasks.base.template:Template",
                "time = scriptengine.tasks.base.time:Time",
                #
                # Valid task names
                "base.chdir = scriptengine.tasks.base.chdir:Chdir",
                "base.command = scriptengine.tasks.base.command:Command",
                "base.context = scriptengine.tasks.base.context:Context",
                "base.context.from = scriptengine.tasks.base.context:ContextFrom",
                "base.copy = scriptengine.tasks.base.file.copy:Copy",
                "base.echo = scriptengine.tasks.base.echo:Echo",
                "base.exit = scriptengine.tasks.base.exit:Exit",
                "base.find = scriptengine.tasks.base.find:Find",
                "base.getenv = scriptengine.tasks.base.envvars:Getenv",
                "base.include = scriptengine.tasks.base.include:Include",
                "base.link = scriptengine.tasks.base.file.link:Link",
                "base.make_dir = scriptengine.tasks.base.file.make_dir:MakeDir",
                "base.move = scriptengine.tasks.base.file.move:Move",
                "base.remove = scriptengine.tasks.base.file.remove:Remove",
                "base.setenv = scriptengine.tasks.base.envvars:Setenv",
                "base.task_timer = scriptengine.tasks.base.task_timer:TaskTimer",
                "base.template = scriptengine.tasks.base.template:Template",
                "base.time = scriptengine.tasks.base.time:Time",
            ],
        },
    )
