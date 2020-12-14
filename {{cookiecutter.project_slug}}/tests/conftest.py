"""Store the classes and fixtures used throughout the tests."""
{% if cookiecutter.read_configuration_from_yaml == "True" -%}
from _pytest.tmpdir import TempdirFactory
import pytest

from shutil import copyfile

from {{cookiecutter.project_underscore_slug}}.config import Config


@pytest.fixture(name="config")
def fixture_config(tmpdir_factory: TempdirFactory) -> Config:
    """Configure the Config object for the tests."""
    data = tmpdir_factory.mktemp("data")
    config_file = str(data.join("config.yaml"))
    copyfile("tests/assets/config.yaml", config_file)
    config = Config(config_file)

    return config
{%- endif %}
