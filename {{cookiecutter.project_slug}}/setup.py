"""Python package building configuration."""

import re
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

# Avoid loading the package to extract the version
with open("src/{{ cookiecutter.project_slug.replace('-', '_') }}/version.py") as fp:
    version_match = re.search(r'__version__ = "(?P<version>.*)"', fp.read())
    if version_match is None:
        raise ValueError("The version is not specified in the version.py file.")
    version = version_match["version"]

setup(
    name="{{ cookiecutter.project_slug }}",
    version=version,
    description="A Cookiecutter template for creating Python projects",
    author="{{ cookiecutter.author}}",
    author_email="{{ cookiecutter.author_email}}",
    license="GNU General Public License v3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/{{ cookiecutter.github_user}}/{{ cookiecutter.project_slug }}",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Natural Language :: English",
    ],
    {%- if cookiecutter.configure_command_line == "True" -%}
    entry_points="""
        [console_scripts]
        {{cookiecutter.project_underscore_slug}}={{cookiecutter.project_underscore_slug}}.entrypoints.cli:cli
    """,
    {%- endif %}
    install_requires=[
        {%- if cookiecutter.requirements != "" -%}
        {% for requirement in cookiecutter.requirements.split(', ') %}'{{ requirement }}', {% endfor %}
        {%- endif -%}
        {%- if cookiecutter.configure_command_line == "True" -%}
        "Click",
        {%- endif -%}
    ],
)
