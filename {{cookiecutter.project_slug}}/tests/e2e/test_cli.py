"""Test the command line interface."""

import logging
import re

import pytest
from _pytest.logging import LogCaptureFixture
from click.testing import CliRunner
from py._path.local import LocalPath
from {{cookiecutter.project_underscore_slug}}.config import Config
from {{cookiecutter.project_underscore_slug}}.entrypoints.cli import cli
from {{cookiecutter.project_underscore_slug}}.version import __version__

{% if cookiecutter.read_configuration_from_yaml == "True" -%}
{%- endif %}


log = logging.getLogger(__name__)

{% if cookiecutter.read_configuration_from_yaml == "True" -%}
@pytest.fixture(name="runner")
def fixture_runner(config: Config) -> CliRunner:
    """Configure the Click cli test runner."""
    return CliRunner(mix_stderr=False, env={"{{cookiecutter.project_underscore_slug | upper}}_CONFIG_PATH": config.config_path})
{% else -%}
@pytest.fixture(name="runner")
def fixture_runner() -> CliRunner:
    """Configure the Click cli test runner."""
    return CliRunner(mix_stderr=False)
{%- endif %}


def test_version(runner: CliRunner) -> None:
    """Prints program version when called with --version."""
    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert re.search(
        fr" *{{ cookiecutter.project_underscore_slug }}: {__version__}\n *Python: .*\n *Platform: .*",
        result.stdout,
    )
{% if cookiecutter.read_configuration_from_yaml == "True" -%}


def test_load_config_handles_configerror_exceptions(
    runner: CliRunner, tmpdir: LocalPath, caplog: LogCaptureFixture
) -> None:
    """
    Given: A wrong configuration file.
    When: CLI is initialized
    Then: The ConfigError exception is gracefully handled.
    """
    config_file = tmpdir.join("config.yaml")  # type: ignore
    config_file.write("[ invalid yaml")

    result = runner.invoke(cli, ["-c", str(config_file), "null"])

    assert result.exit_code == 1
    assert (
        "{{cookiecutter.project_underscore_slug}}.entrypoints",
        logging.ERROR,
        f'Configuration Error: while parsing a flow sequence\n  in "{config_file}", '
        "line 1, column 1\nexpected ',' or ']', but got '<stream end>'\n  in"
        f' "{config_file}", line 1, column 15',
    ) in caplog.record_tuples
{%- endif %}
