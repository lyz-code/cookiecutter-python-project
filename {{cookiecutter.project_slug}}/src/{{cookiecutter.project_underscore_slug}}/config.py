"""Define the configuration of the main program."""

{% if cookiecutter.read_configuration_from_yaml == "True" -%}
import logging
import os
from collections import UserDict
from typing import Any, Dict, List, Union

from ruamel.yaml import YAML

log = logging.getLogger(__name__)


# R0901: UserDict has too many ancestors. Right now I don't feel like switching to
#   another base class, as `dict` won't work straight ahead.
class Config(UserDict):  # noqa: R0901
    """Expose the configuration in a friendly way.

    Public methods:
        get: Fetch the configuration value of the specified key.
        load: Load the configuration from the configuration YAML file.
        save: Saves the configuration in the configuration YAML file.

    Attributes and properties:
        config_path (str): Path to the configuration file.
        data(dict): Program configuration.
    """

    def __init__(
        self,
        config_path: str = "~/.local/share/{{ cookiecutter.project_underscore_slug}}/config.yaml"
    ) -> None:
        """Configure the attributes and load the configuration."""
        super().__init__()
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
        config_keys = key.split(".")
        value = self.data.copy()

        for config_key in config_keys:
            try:
                value = value[config_key]
            except KeyError as error:
                raise KeyError(
                    f"Failed to fetch the configuration {config_key} "
                    f"when searching for {original_key}"
                ) from error

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
        if not isinstance(parent, dict):
            raise ValueError("No configuration is found under the path {key}")
        parent[keys[-1]] = value

    def load(self) -> None:
        """Load the configuration from the configuration YAML file."""
        with open(os.path.expanduser(self.config_path), "r") as file_cursor:
            self.data = YAML().load(file_cursor)

    def save(self) -> None:
        """Save the configuration in the configuration YAML file."""
        with open(os.path.expanduser(self.config_path), "w+") as file_cursor:
            yaml = YAML()
            yaml.default_flow_style = False
            yaml.dump(self.data, file_cursor)
{%- endif %}
