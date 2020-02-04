import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scriptengine",
    version="0.3.1",
    author="Uwe Fladrich",
    author_email="uwe.fladrich@protonmail.com",
    description="A funny package for configuring and running tasks",
    long_description=long_description,
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
          'deepmerge',
          'pyaml',
          'jinja2',
      ],
    scripts=['bin/se'],
)
