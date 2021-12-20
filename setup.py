import codecs
import os

import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]


setuptools.setup(
    name="scriptengine",
    version=get_version("scriptengine/version.py"),
    author="Uwe Fladrich",
    author_email="uwe.fladrich@protonmail.com",
    description="A lightweight and extensible framework for executing "
    "scripts written in YAML",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/uwefladrich/scriptengine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "python-dateutil",
        "deepmerge",
        "deepdiff>=5.7.0",
        "PyYAML",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "se = scriptengine.cli.se:main",
        ],
        "scriptengine.tasks": [
            # Short aliases for backward compatibility
            "chdir = scriptengine.tasks.base.chdir:Chdir",
            "command = scriptengine.tasks.base.command:Command",
            "context = scriptengine.tasks.base.context:Context",
            "copy = scriptengine.tasks.base.file:Copy",
            "echo = scriptengine.tasks.base.echo:Echo",
            "exit = scriptengine.tasks.base.exit:Exit",
            "find = scriptengine.tasks.base.find:Find",
            "include = scriptengine.tasks.base.include:Include",
            "link = scriptengine.tasks.base.file:Link",
            "make_dir = scriptengine.tasks.base.file:MakeDir",
            "move = scriptengine.tasks.base.file:Move",
            "remove = scriptengine.tasks.base.file:Remove",
            "task_timer = scriptengine.tasks.base.task_timer:TaskTimer",
            "template = scriptengine.tasks.base.template:Template",
            "time = scriptengine.tasks.base.time:Time",
            # Real names
            "base.chdir = scriptengine.tasks.base.chdir:Chdir",
            "base.command = scriptengine.tasks.base.command:Command",
            "base.context = scriptengine.tasks.base.context:Context",
            "base.copy = scriptengine.tasks.base.file:Copy",
            "base.echo = scriptengine.tasks.base.echo:Echo",
            "base.exit = scriptengine.tasks.base.exit:Exit",
            "base.find = scriptengine.tasks.base.find:Find",
            "base.getenv = scriptengine.tasks.base.envvars:Getenv",
            "base.include = scriptengine.tasks.base.include:Include",
            "base.link = scriptengine.tasks.base.file:Link",
            "base.make_dir = scriptengine.tasks.base.file:MakeDir",
            "base.move = scriptengine.tasks.base.file:Move",
            "base.remove = scriptengine.tasks.base.file:Remove",
            "base.setenv = scriptengine.tasks.base.envvars:Setenv",
            "base.task_timer = scriptengine.tasks.base.task_timer:TaskTimer",
            "base.template = scriptengine.tasks.base.template:Template",
            "base.time = scriptengine.tasks.base.time:Time",
        ],
    },
)
