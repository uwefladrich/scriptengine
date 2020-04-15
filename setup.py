import os
import codecs
import setuptools

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

setuptools.setup(
    name="scriptengine",
    version=get_version("scriptengine/__init__.py"),
    author="Uwe Fladrich",
    author_email="uwe.fladrich@protonmail.com",
    description="A better way to configure and run things that usually go into shell scripts",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/uwefladrich/scriptengine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'python-dateutil',
          'deepmerge',
          'PyYAML',
          'jinja2',
      ],
    scripts=['bin/se'],
)
