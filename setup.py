"""Python package building configuration."""

from setuptools import setup

__version__: str = "0.1.0"

setup(
    name="cookiecutter-python-project",
    version=__version__,
    description="A Cookiecutter template for creating Python projects",
    author="Lyz",
    author_email="lyz-code-security-advisories@riseup.net",
    license="GNU General Public License v3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lyz-code/cookiecutter-python-project",
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
        "cookiecutter",
        # https://github.com/hackebrot/pytest-cookies/issues/50
        "arrow<0.14.0",
        "sh",
        "passpy",
        "pynacl",
    ],
)
