"""Test the configuration of the program."""

import re

import pytest
from {{cookiecutter.project_underscore_slug}}.config import Config


def test_config_load(config: Config) -> None:
    """Loading the configuration from the yaml file works."""
    config.load()  # act

    assert config.data["verbose"] == "info"


def test_save_config(config: Config) -> None:
    """Saving the configuration to the yaml file works."""
    config.data = {"a": "b"}

    config.save()  # act

    with open(config.config_path, "r") as file_cursor:
        assert "a:" in file_cursor.read()


def test_get_can_fetch_nested_items_with_dots(config: Config) -> None:
    """Fetching values of configuration keys using dot notation works."""
    config.data = {
        "first": {"second": "value"},
    }

    result = config.get("first.second")

    assert result == "value"


def test_config_can_fetch_nested_items_with_dictionary_notation(config: Config) -> None:
    """Fetching values of configuration keys using the dictionary notation works."""
    config.data = {
        "first": {"second": "value"},
    }

    result = config["first"]["second"]

    assert result == "value"


def test_get_an_unexistent_key_raises_error(config: Config) -> None:
    """If the key you're trying to fetch doesn't exist, raise a KeyError exception."""
    config.data = {
        "reports": {"second": "value"},
    }

    with pytest.raises(KeyError) as error:
        config.get("reports.inexistent")


def test_set_can_set_nested_items_with_dots(config: Config) -> None:
    """Setting values of configuration keys using dot notation works."""
    config.set("storage.type", "tinydb")  # act

    result = config.data["storage"]["type"]

    assert result == "tinydb"
