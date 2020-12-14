"""Define the configuration of the main program."""

{% if cookiecutter.read_configuration_from_yaml == "True" -%}
import logging
import os
from collections import UserDict
from typing import Any, Dict, List, Union

from ruamel.yaml import YAML

log = logging.getLogger(__name__)


class Config(UserDict):
    """Expose the configuration in a friendly way.

    Public methods:
        get: Fetch the configuration value of the specified key.
        load: Load the configuration from the configuration YAML file.
        save: Saves the configuration in the configuration YAML file.

    Attributes and properties:
        config_path (str): Path to the configuration file.
        data(dict): Program configuration.
    """

    def __init__(self, config_path="~/.local/share/{{ cookiecutter.project_underscore_slug}}/config.yaml"):
        """Configure the attributes and load the configuration."""
        self.config_path = os.path.expanduser(config_path)
        self.load()

    def get(self, key: str, default: Any = None) -> Union[str, int, Dict, List]:
        """Fetch the configuration value of the specified key.

        If there are nested dictionaries, a dot notation can be used.

        So if the configuration contents are:

        self.data = {
            'first': {
                'second': 'value'
            },
        }

        self.data.get('first.second') == 'value'
        """
        original_key = key
        keys = key.split(".")
        value = self.data.copy()

        for key in keys:
            try:
                value = value[key]
            except KeyError:
                raise KeyError(
                    f"Failed to fetch the configuration {key} "
                    f"when searching for {original_key}"
                )

        return value

    def set(self, key: str, value: Union[str, int]) -> None:
        """Set the configuration value of the specified key.

        If there are nested dictionaries, a dot notation can be used.

        So if you want to set the configuration:

        self.data = {
            'first': {
                'second': 'value'
            },
        }

        self.data.set('first.second', 'value')
        """
        keys: List = key.split(".")

        parent = self.get(".".join(keys[:-1]))
        if isinstance(parent, dict):
            parent[keys[-1]] = value
        else:
            raise ValueError("No configuration is found under the path {key}")

    def load(self) -> None:
        """Load the configuration from the configuration YAML file."""

        with open(os.path.expanduser(self.config_path), "r") as f:
            self.data = YAML().load(f)

    def save(self):
        """Save the configuration in the configuration YAML file."""

        with open(os.path.expanduser(self.config_path), "w+") as f:
            yaml = YAML()
            yaml.default_flow_style = False
            yaml.dump(self.data, f)
{%- endif %}
