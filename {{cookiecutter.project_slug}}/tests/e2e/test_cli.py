"""Test the command line interface."""

import logging
import re

import pytest
from click.testing import CliRunner
from {{cookiecutter.project_underscore_slug}}.entrypoints.cli import cli
from {{cookiecutter.project_underscore_slug}}.version import __version__
from {{cookiecutter.project_underscore_slug}}.config import Config
from _pytest.logging import LogCaptureFixture
{% if cookiecutter.read_configuration_from_yaml == "True" -%}
from shutil import copyfile
from py._path.local import LocalPath
from _pytest.tmpdir import TempdirFactory
{%- endif %}


{% if cookiecutter.read_configuration_from_yaml == "True" -%}
@pytest.fixture(name="config")
def fixture_config(tmpdir_factory: TempdirFactory) -> Config:
    """Configure the Config object for the tests."""
    data = tmpdir_factory.mktemp("data")
    config_file = str(data.join("config.yaml"))
    copyfile("assets/config.yaml", config_file)
    config = Config(config_file)

    return config
{%- endif %}


{% if cookiecutter.read_configuration_from_yaml == "True" -%}
@pytest.fixture(name="runner")
def fixture_runner(config) -> CliRunner:
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
    assert re.match(
        fr" *{{ cookiecutter.project_underscore_slug }} version: {__version__}\n"
        r" *python version: .*\n *platform: .*",
        result.stdout,
    )
{% if cookiecutter.read_configuration_from_yaml == "True" -%}


def test_load_config_handles_wrong_file_format(
    runner: CliRunner,
    tmpdir: LocalPath,
    caplog: LogCaptureFixture
) -> None:
    """Capture the error of a wrong configuration file."""
    config_file = tmpdir.join("config.yaml")
    config_file.write("[ invalid yaml")

    result = runner.invoke(cli, ["-c", str(config_file), "null"])

    assert result.exit_code == 1
    assert (
        "{{cookiecutter.project_underscore_slug}}.entrypoints",
        logging.ERROR,
        f"Error parsing yaml of configuration file {config_file}: expected ',' or"
        " ']', but got '<stream end>'",
    ) in caplog.record_tuples


def test_load_handles_file_not_found(
    runner: CliRunner,
    tmpdir: LocalPath,
    caplog: LogCaptureFixture
) -> None:
    """Capture the error of a missing configuration file."""
    config_file = tmpdir.join("unexistent_config.yaml")

    result = runner.invoke(cli, ["-c", str(config_file), "null"])

    assert result.exit_code == 1
    assert (
        "{{cookiecutter.project_underscore_slug}}.entrypoints",
        logging.ERROR,
        f"Error opening configuration file {config_file}",
    ) in caplog.record_tuples
{%- endif %}
