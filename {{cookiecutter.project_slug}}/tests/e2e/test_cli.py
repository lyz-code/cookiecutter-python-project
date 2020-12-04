"""Test the command line interface."""

import re

import pytest
from click.testing import CliRunner
from {{cookiecutter.project_underscore_slug}}.entrypoints.cli import cli
from {{cookiecutter.project_underscore_slug}}.version import __version__


@pytest.fixture(name="runner")
def fixture_runner() -> CliRunner:
    """Configure the Click cli test runner."""
    return CliRunner(mix_stderr=False)


def test_version(runner: CliRunner) -> None:
    """Prints program version when called with --version."""
    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert re.match(
        fr" *{{ cookiecutter.project_underscore_slug }} version: {__version__}\n"
        r" *python version: .*\n *platform: .*",
        result.stdout,
    )
