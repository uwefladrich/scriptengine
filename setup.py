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
        version="1.0.0rc1",
        install_requires=[
            "python-dateutil",
            "deepmerge",
            "PyYAML",
            "jinja2",
        ],
        extras_require={"tests": tests, "docs": docs, "all": tests + docs},
        entry_points={
            "console_scripts": [
                "se = scriptengine.cli.se:main",
            ],
            "scriptengine.tasks": [
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
