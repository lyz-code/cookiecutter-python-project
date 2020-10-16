from setuptools import find_packages, setup

__version__ = "0.1.0"

setup(
    name="cookiecutter-python-project",
    version=__version__,  # noqa: F821
    description="A Cookiecutter template for creating Python projects",
    author="Lyz",
    author_email="lyz@riseup.net",
    license="GPLv3",
    long_description=open("README.md").read(),
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "cookiecutter",
        # https://github.com/hackebrot/pytest-cookies/issues/50
        "arrow<0.14.0",
        "sh",
        "passpy",
        "pynacl",
    ],
)
