"""Python package building configuration."""

from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="cookiecutter-python-project",
    description="A Cookiecutter template for creating Python projects",
    author="Lyz",
    author_email="lyz-code-security-advisories@riseup.net",
    license="GNU General Public License v3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lyz-code/cookiecutter-python-project",
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
    install_requires=[
        "arrow<0.14.0",  # https://github.com/hackebrot/pytest-cookies/issues/50
        "cookiecutter",
        "cryptography",
        "passpy",
        "pynacl",
        "sh",
    ],
)
