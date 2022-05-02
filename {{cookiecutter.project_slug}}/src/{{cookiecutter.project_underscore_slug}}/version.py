"""Utilities to retrieve the information of the program version."""

import platform
import sys

# Do not edit the version manually, let `make bump` do it.

__version__ = "0.1.0"


def version_info() -> str:
    """Display the version of the program, python and the platform."""
    return dedent(
        f"""\
        ------------------------------------------------------------------
             {{cookiecutter.project_underscore_slug}}: {__version__}
             Python: {python_version}
             Platform: {platform.platform()}
        ------------------------------------------------------------------"""
    )
