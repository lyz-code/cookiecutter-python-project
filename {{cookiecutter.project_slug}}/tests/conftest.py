"""Store the classes and fixtures used throughout the tests."""
{% if cookiecutter.read_configuration_from_yaml == "True" -%}
import pytest
from _pytest.tmpdir import TempdirFactory
from {{cookiecutter.project_underscore_slug}}.config import Config


@pytest.fixture(name="config")
def fixture_config(tmpdir_factory: TempdirFactory) -> Config:
    """Configure the program for the tests."""
    # Once https://github.com/lincolnloop/goodconf/issues/10 is solved prepend
    # the environment variables with the program prefix
    # to configure it use os.environ["DEBUG"] = 'True'

    return Config(load=True)
{%- endif %}
