"""Utilities to retrieve the information of the program version."""

import platform
import sys
from textwrap import dedent

# Do not edit the version manually, let `make bump` do it.

__version__ = "0.1.0"


def version_info() -> str:
    """Display the version of the program, python and the platform."""
    return dedent(
        f"""\
        ------------------------------------------------------------------
             {{cookiecutter.project_underscore_slug}}: {__version__}
             Python: {sys.version.split(" ", maxsplit=1)[0]}
             Platform: {platform.platform()}
        ------------------------------------------------------------------"""
    )
